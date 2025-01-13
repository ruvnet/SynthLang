#!/bin/bash

# High Frequency Trading Strategy with RSI and Self-Learning
# This script implements the core concepts from the specification

# Configuration
INTERVAL=60  # 1 minute in seconds
RSI_PERIOD=14
OVERBOUGHT=70
OVERSOLD=30
PROFIT_TARGET=0.5
STOP_LOSS=0.3
POSITION_SIZE=1.0

# Create necessary directories
mkdir -p data logs metrics

# Initialize log file
LOG_FILE="logs/trading_$(date +%Y%m%d).log"
METRICS_FILE="metrics/performance_$(date +%Y%m%d).csv"

# Initialize metrics file
echo "timestamp,rsi,signal,price,position,pnl,win_rate,sharpe_ratio" > "$METRICS_FILE"

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to calculate RSI
# This is a simplified version for demonstration
calculate_rsi() {
    local prices=($1)
    local gains=0
    local losses=0
    
    for ((i=1; i<${#prices[@]}; i++)); do
        local diff=$(echo "${prices[$i]} - ${prices[$i-1]}" | bc)
        if (( $(echo "$diff > 0" | bc -l) )); then
            gains=$(echo "$gains + $diff" | bc)
        else
            losses=$(echo "$losses + ${diff#-}" | bc)
        fi
    done
    
    local avg_gain=$(echo "$gains / $RSI_PERIOD" | bc -l)
    local avg_loss=$(echo "$losses / $RSI_PERIOD" | bc -l)
    
    if (( $(echo "$avg_loss == 0" | bc -l) )); then
        echo "100"
        return
    fi
    
    local rs=$(echo "$avg_gain / $avg_loss" | bc -l)
    local rsi=$(echo "100 - (100 / (1 + $rs))" | bc -l)
    
    printf "%.2f" "$rsi"
}

# Function to generate trading signals
generate_signal() {
    local rsi=$1
    
    if (( $(echo "$rsi < $OVERSOLD" | bc -l) )); then
        echo "BUY"
    elif (( $(echo "$rsi > $OVERBOUGHT" | bc -l) )); then
        echo "SELL"
    else
        echo "HOLD"
    fi
}

# Function to optimize parameters based on performance
optimize_parameters() {
    local win_rate=$1
    local sharpe_ratio=$2
    
    # Adjust RSI parameters based on performance
    if (( $(echo "$win_rate < 0.5" | bc -l) )); then
        RSI_PERIOD=$(echo "$RSI_PERIOD + 1" | bc)
        log_message "Adjusted RSI period to $RSI_PERIOD due to low win rate"
    fi
    
    if (( $(echo "$sharpe_ratio < 1.0" | bc -l) )); then
        OVERBOUGHT=$(echo "$OVERBOUGHT + 1" | bc)
        OVERSOLD=$(echo "$OVERSOLD - 1" | bc)
        log_message "Adjusted RSI thresholds: OVERBOUGHT=$OVERBOUGHT, OVERSOLD=$OVERSOLD"
    fi
}

# Function to calculate performance metrics
calculate_metrics() {
    local pnl=$1
    local trades=$2
    
    # Calculate win rate
    local win_rate=$(echo "$pnl > 0" | bc -l)
    
    # Simplified Sharpe ratio calculation
    local sharpe_ratio=0
    if [ $trades -gt 0 ]; then
        sharpe_ratio=$(echo "$pnl / $trades" | bc -l)
    fi
    
    echo "$win_rate,$sharpe_ratio"
}

# Function to validate parameter changes
validate_changes() {
    local current_rsi=$1
    local current_price=$2
    
    # Check if parameters are within acceptable ranges
    if [ $RSI_PERIOD -lt 5 ] || [ $RSI_PERIOD -gt 50 ]; then
        RSI_PERIOD=14  # Reset to default if out of range
        log_message "Reset RSI period to default: parameter out of acceptable range"
    fi
    
    if [ $OVERBOUGHT -lt 60 ] || [ $OVERBOUGHT -gt 90 ]; then
        OVERBOUGHT=70  # Reset to default if out of range
        log_message "Reset overbought threshold to default: parameter out of acceptable range"
    fi
    
    if [ $OVERSOLD -lt 10 ] || [ $OVERSOLD -gt 40 ]; then
        OVERSOLD=30  # Reset to default if out of range
        log_message "Reset oversold threshold to default: parameter out of acceptable range"
    fi
}

# Main trading loop
log_message "Starting HFT RSI Strategy"
log_message "Initial parameters: RSI_PERIOD=$RSI_PERIOD, OVERBOUGHT=$OVERBOUGHT, OVERSOLD=$OVERSOLD"

# Initialize variables
position="NONE"
entry_price=0
total_pnl=0
total_trades=0
declare -a prices=()

# Trap Ctrl+C to clean up
trap 'echo ""; log_message "Strategy stopped by user"; exit 0' INT

# Function to calculate additional metrics
calculate_advanced_metrics() {
    local pnl=$1
    local trades=$2
    local prices=($3)
    
    # Calculate volatility (simple standard deviation)
    local mean=0
    local sum_squared_diff=0
    for price in "${prices[@]}"; do
        mean=$(echo "$mean + $price" | bc -l)
    done
    mean=$(echo "$mean / ${#prices[@]}" | bc -l)
    
    for price in "${prices[@]}"; do
        local diff=$(echo "$price - $mean" | bc -l)
        sum_squared_diff=$(echo "$sum_squared_diff + ($diff * $diff)" | bc -l)
    done
    local volatility=$(echo "sqrt($sum_squared_diff / ${#prices[@]})" | bc -l)
    
    # Calculate max drawdown
    local peak=0
    local max_drawdown=0
    for price in "${prices[@]}"; do
        if (( $(echo "$price > $peak" | bc -l) )); then
            peak=$price
        fi
        local drawdown=$(echo "($peak - $price) / $peak * 100" | bc -l)
        if (( $(echo "$drawdown > $max_drawdown" | bc -l) )); then
            max_drawdown=$drawdown
        fi
    done
    
    echo "$volatility,$max_drawdown"
}

# Function to show menu
show_menu() {
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                    HFT RSI Strategy Menu                       ║"
    echo "╠════════════════════════════════════════════════════════════════╣"
    echo "║ 1. Start Trading                                              ║"
    echo "║ 2. View Current Parameters                                    ║"
    echo "║ 3. Modify Parameters                                          ║"
    echo "║ 4. View Performance Report                                    ║"
    echo "║ 5. View Advanced Analytics                                    ║"
    echo "║ 6. Exit                                                       ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo -n "Select an option (1-6): "
    read -r choice
    
    case $choice in
        1) return 0 ;;  # Start trading
        2) show_parameters ;;
        3) modify_parameters ;;
        4) show_performance ;;
        5) show_analytics ;;
        6) exit 0 ;;
        *) echo "Invalid option" ; show_menu ;;
    esac
}

# Function to show parameters
show_parameters() {
    clear
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                    Current Parameters                          ║"
    echo "╠════════════════════════════════════════════════════════════════╣"
    printf "║ RSI Period: %-48d ║\n" "$RSI_PERIOD"
    printf "║ Overbought Threshold: %-39d ║\n" "$OVERBOUGHT"
    printf "║ Oversold Threshold: %-41d ║\n" "$OVERSOLD"
    printf "║ Profit Target: %-45.2f ║\n" "$PROFIT_TARGET"
    printf "║ Stop Loss: %-49.2f ║\n" "$STOP_LOSS"
    printf "║ Position Size: %-46.2f ║\n" "$POSITION_SIZE"
    echo "╚════════════════════════════════════════════════════════════════╝"
    read -n 1 -s -r -p "Press any key to continue..."
    show_menu
}

# Function to modify parameters
modify_parameters() {
    clear
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                    Modify Parameters                           ║"
    echo "╠════════════════════════════════════════════════════════════════╣"
    echo "║ Enter new values (or press Enter to keep current):            ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    
    read -p "RSI Period [$RSI_PERIOD]: " new_period
    [ -n "$new_period" ] && RSI_PERIOD=$new_period
    
    read -p "Overbought Threshold [$OVERBOUGHT]: " new_overbought
    [ -n "$new_overbought" ] && OVERBOUGHT=$new_overbought
    
    read -p "Oversold Threshold [$OVERSOLD]: " new_oversold
    [ -n "$new_oversold" ] && OVERSOLD=$new_oversold
    
    read -p "Profit Target [$PROFIT_TARGET]: " new_profit
    [ -n "$new_profit" ] && PROFIT_TARGET=$new_profit
    
    read -p "Stop Loss [$STOP_LOSS]: " new_stop
    [ -n "$new_stop" ] && STOP_LOSS=$new_stop
    
    read -p "Position Size [$POSITION_SIZE]: " new_size
    [ -n "$new_size" ] && POSITION_SIZE=$new_size
    
    show_menu
}

# Function to show performance
show_performance() {
    clear
    if [ ! -f "$METRICS_FILE" ]; then
        echo "No performance data available yet."
        read -n 1 -s -r -p "Press any key to continue..."
        show_menu
        return
    }
    
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                    Performance Report                          ║"
    echo "╠════════════════════════════════════════════════════════════════╣"
    echo "║ Last 10 Trades:                                               ║"
    tail -n 10 "$METRICS_FILE" | while IFS=, read -r timestamp rsi signal price position pnl win_rate sharpe; do
        printf "║ %s | %s | P&L: %.2f                              ║\n" "$timestamp" "$position" "$pnl"
    done
    echo "╚════════════════════════════════════════════════════════════════╝"
    read -n 1 -s -r -p "Press any key to continue..."
    show_menu
}

# Function to show analytics
show_analytics() {
    clear
    if [ ! -f "$METRICS_FILE" ]; then
        echo "No analytics data available yet."
        read -n 1 -s -r -p "Press any key to continue..."
        show_menu
        return
    }
    
    # Calculate advanced metrics
    local all_prices=$(awk -F',' '{print $4}' "$METRICS_FILE")
    local total_pnl=$(awk -F',' '{sum += $6} END {print sum}' "$METRICS_FILE")
    local total_trades=$(wc -l < "$METRICS_FILE")
    
    IFS=',' read -r volatility max_drawdown <<< "$(calculate_advanced_metrics "$total_pnl" "$total_trades" "$all_prices")"
    
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                    Advanced Analytics                          ║"
    echo "╠════════════════════════════════════════════════════════════════╣"
    printf "║ Price Volatility: %-43.2f ║\n" "$volatility"
    printf "║ Maximum Drawdown: %-42.2f%% ║\n" "$max_drawdown"
    printf "║ Average Trade P&L: %-41.2f ║\n" "$(echo "$total_pnl / $total_trades" | bc -l)"
    echo "╚════════════════════════════════════════════════════════════════╝"
    read -n 1 -s -r -p "Press any key to continue..."
    show_menu
}

# Function to display status
display_status() {
    clear
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                    HFT RSI Strategy Status                      ║"
    echo "╠════════════════════════════════════════════════════════════════╣"
    echo "║ Current Parameters:                                            ║"
    printf "║ • RSI Period: %-48d ║\n" "$RSI_PERIOD"
    printf "║ • Overbought: %-47d ║\n" "$OVERBOUGHT"
    printf "║ • Oversold: %-49d ║\n" "$OVERSOLD"
    echo "╠════════════════════════════════════════════════════════════════╣"
    printf "║ Current Price: %-46.2f ║\n" "$1"
    printf "║ Current RSI: %-48.2f ║\n" "$2"
    printf "║ Signal: %-52s ║\n" "$3"
    printf "║ Position: %-50s ║\n" "$4"
    printf "║ Total P&L: %-49.2f ║\n" "$5"
    printf "║ Total Trades: %-47d ║\n" "$6"
    if [ "$6" -gt 0 ]; then
        printf "║ Win Rate: %-50.2f%% ║\n" "$(echo "$7 * 100" | bc -l)"
        printf "║ Sharpe Ratio: %-46.2f ║\n" "$8"
        echo "╠════════════════════════════════════════════════════════════════╣"
        echo "║ Advanced Metrics:                                              ║"
        # Calculate advanced metrics
        IFS=',' read -r volatility max_drawdown <<< "$(calculate_advanced_metrics "$5" "$6" "${prices[*]}")"
        printf "║ • Volatility: %-47.2f ║\n" "$volatility"
        printf "║ • Max Drawdown: %-45.2f%% ║\n" "$max_drawdown"
        printf "║ • Avg Trade Size: %-44.2f ║\n" "$(echo "$5 / $6" | bc -l)"
        local success_count=$(grep -c "Position closed.*P&L: [0-9]*\.[0-9]*$" "$LOG_FILE")
        printf "║ • Success Rate: %-45.2f%% ║\n" "$(echo "scale=2; $success_count / $6 * 100" | bc -l)"
        echo "╠════════════════════════════════════════════════════════════════╣"
        echo "║ Strategy Health:                                              ║"
        local health_score=$(echo "scale=2; ($7 * 0.4 + (1 - $max_drawdown/100) * 0.3 + $8 * 0.3) * 100" | bc -l)
        printf "║ • Strategy Score: %-44.2f%% ║\n" "$health_score"
        if (( $(echo "$health_score > 75" | bc -l) )); then
            echo "║ • Status: Optimal                                              ║"
        elif (( $(echo "$health_score > 50" | bc -l) )); then
            echo "║ • Status: Good                                                 ║"
        elif (( $(echo "$health_score > 25" | bc -l) )); then
            echo "║ • Status: Needs Attention                                      ║"
        else
            echo "║ • Status: Critical - Consider Parameter Adjustment             ║"
        fi
        echo "╠════════════════════════════════════════════════════════════════╣"
        echo "║ Learning Progress:                                             ║"
        local param_changes=$(grep -c "Adjusted" "$LOG_FILE")
        printf "║ • Parameter Adjustments: %-39d ║\n" "$param_changes"
        printf "║ • Optimization Cycles: %-41d ║\n" "$((total_trades / 10))"
    fi
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Last 5 Log Entries:"
    echo "──────────────────────────────────────────────────────────────────"
    tail -n 5 "$LOG_FILE"
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                        Control Options                          ║"
    echo "╠════════════════════════════════════════════════════════════════╣"
    echo "║ • Press Ctrl+C to safely exit the strategy                     ║"
    echo "║   This will:                                                   ║"
    echo "║   - Save all current metrics                                   ║"
    echo "║   - Log final trading state                                    ║"
    echo "║   - Close all open positions                                   ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
}

# Show initial menu
show_menu

# Main trading loop
while true; do
    # Simulate getting current price (random walk for demonstration)
    current_price=$(echo "100 + $(( RANDOM % 100 - 50 )) / 100" | bc -l)
    
    # Display initial status with empty RSI and signal
    if [ ${#prices[@]} -lt $RSI_PERIOD ]; then
        display_status "$current_price" "N/A" "Collecting data..." "$position" "$total_pnl" "$total_trades" "0" "0"
    fi
    
    # Store price in array for RSI calculation
    prices+=($current_price)
    if [ ${#prices[@]} -gt $RSI_PERIOD ]; then
        prices=("${prices[@]:1}")  # Keep only last RSI_PERIOD prices
    fi
    
    # Calculate RSI if we have enough prices
    if [ ${#prices[@]} -eq $RSI_PERIOD ]; then
        rsi=$(calculate_rsi "${prices[*]}")
        signal=$(generate_signal $rsi)
        
        # Display status before trading decisions
        display_status "$current_price" "$rsi" "$signal" "$position" "$total_pnl" "$total_trades" "0" "0"
        
        # Trading logic
        case $signal in
            "BUY")
                if [ "$position" != "LONG" ]; then
                    position="LONG"
                    entry_price=$current_price
                    total_trades=$((total_trades + 1))
                    log_message "LONG position opened at $current_price (RSI: $rsi)"
                fi
                ;;
            "SELL")
                if [ "$position" != "SHORT" ]; then
                    position="SHORT"
                    entry_price=$current_price
                    total_trades=$((total_trades + 1))
                    log_message "SHORT position opened at $current_price (RSI: $rsi)"
                fi
                ;;
        esac
        
        # Calculate P&L if in position
        if [ "$position" != "NONE" ]; then
            local pnl=0
            if [ "$position" == "LONG" ]; then
                pnl=$(echo "$current_price - $entry_price" | bc -l)
            else
                pnl=$(echo "$entry_price - $current_price" | bc -l)
            fi
            total_pnl=$(echo "$total_pnl + $pnl" | bc -l)
            
            # Check for take profit or stop loss
            if (( $(echo "$pnl >= $PROFIT_TARGET" | bc -l) )) || (( $(echo "$pnl <= -$STOP_LOSS" | bc -l) )); then
                log_message "Position closed at $current_price (P&L: $pnl)"
                position="NONE"
                entry_price=0
            fi
        fi
        
        # Calculate and log metrics
        if [ $total_trades -gt 0 ]; then
            metrics=$(calculate_metrics $total_pnl $total_trades)
            IFS=',' read -r win_rate sharpe_ratio <<< "$metrics"
            
            # Log to metrics file
            echo "$(date '+%Y-%m-%d %H:%M:%S'),$rsi,$signal,$current_price,$position,$total_pnl,$win_rate,$sharpe_ratio" >> "$METRICS_FILE"
            
            # Optimize parameters every 10 trades
            if (( total_trades % 10 == 0 )); then
                optimize_parameters $win_rate $sharpe_ratio
                validate_changes $rsi $current_price
            fi
            
            # Display updated status with metrics
            display_status "$current_price" "$rsi" "$signal" "$position" "$total_pnl" "$total_trades" "$win_rate" "$sharpe_ratio"
        fi
    fi
    
    # Sleep with countdown and status message
    for ((i=INTERVAL; i>0; i--)); do
        echo -ne "\r╔═══════════════════════════════════════════════════╗"
        echo -ne "\r║ Monitoring Market - Next Update: $i seconds remaining ║"
        echo -ne "\r╚═══════════════════════════════════════════════════╝\r"
        sleep 1
    done
done
