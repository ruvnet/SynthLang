#!/bin/bash

# High Frequency Trading Strategy with RSI and Self-Learning
# Enhanced with Mathematical Patterns

# Configuration (Set Theory: Parameter Space)
# ↹ parameters•constraints
# ⊕ define => boundaries
# Σ configuration
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

# Initialize metrics file with enhanced fields
echo "timestamp,rsi,signal,price,position,pnl,win_rate,sharpe_ratio,risk_adjusted_return,volatility" > "$METRICS_FILE"

# Function to log messages with pattern annotations
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to calculate RSI using Category Theory patterns
# ↹ price•series
# ⊕ transform => momentum
# Σ indicator
calculate_rsi() {
    local prices=($1)
    local gains=0
    local losses=0
    
    # Category Theory: Transform price differences to gain/loss categories
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

# Function to generate trading signals using Topology patterns
# ↹ rsi•boundaries
# ⊕ classify => regions
# Σ signal
generate_signal() {
    local rsi=$1
    
    # Topology: Define signal regions with continuous boundaries
    if (( $(echo "$rsi < $OVERSOLD" | bc -l) )); then
        echo "BUY"
    elif (( $(echo "$rsi > $OVERBOUGHT" | bc -l) )); then
        echo "SELL"
    else
        echo "HOLD"
    fi
}

# Function to calculate performance metrics using mathematical patterns
# ↹ trades•outcomes
# ⊕ analyze => metrics
# Σ performance
calculate_metrics() {
    local pnl=$1
    local trades=$2
    local prices=($3)
    
    # Set Theory: Partition trades into success/failure sets
    local win_rate=$(echo "$pnl > 0" | bc -l)
    
    # Category Theory: Transform trade data to risk metrics
    local sharpe_ratio=0
    if [ $trades -gt 0 ]; then
        sharpe_ratio=$(echo "$pnl / $trades" | bc -l)
    fi
    
    # Topology: Calculate continuous risk measures
    local volatility=0
    local mean=0
    for price in "${prices[@]}"; do
        mean=$(echo "$mean + $price" | bc -l)
    done
    mean=$(echo "$mean / ${#prices[@]}" | bc -l)
    
    for price in "${prices[@]}"; do
        local diff=$(echo "$price - $mean" | bc -l)
        volatility=$(echo "$volatility + ($diff * $diff)" | bc -l)
    done
    volatility=$(echo "sqrt($volatility / ${#prices[@]})" | bc -l)
    
    # Calculate risk-adjusted return
    local risk_adjusted_return=0
    if [ $trades -gt 0 ]; then
        risk_adjusted_return=$(echo "$pnl / (1 + $volatility)" | bc -l)
    fi
    
    echo "$win_rate,$sharpe_ratio,$risk_adjusted_return,$volatility"
}

# Function to optimize parameters using mathematical patterns
# ↹ metrics•parameters
# ⊕ optimize => adjustments
# Σ improved
optimize_parameters() {
    local win_rate=$1
    local sharpe_ratio=$2
    local risk_adjusted_return=$3
    local volatility=$4
    
    # Category Theory: Transform performance metrics to parameter adjustments
    if (( $(echo "$win_rate < 0.5" | bc -l) )); then
        RSI_PERIOD=$(echo "$RSI_PERIOD + 1" | bc)
        log_message "Adjusted RSI period to $RSI_PERIOD (Category: Performance Transform)"
    fi
    
    # Topology: Continuous parameter adjustment based on risk metrics
    if (( $(echo "$sharpe_ratio < 1.0" | bc -l) )); then
        OVERBOUGHT=$(echo "$OVERBOUGHT + 1" | bc)
        OVERSOLD=$(echo "$OVERSOLD - 1" | bc)
        log_message "Adjusted thresholds: OVERBOUGHT=$OVERBOUGHT, OVERSOLD=$OVERSOLD (Topology: Risk Adaptation)"
    fi
    
    # Set Theory: Adjust position sizing based on volatility
    if (( $(echo "$volatility > 2.0" | bc -l) )); then
        POSITION_SIZE=$(echo "$POSITION_SIZE * 0.9" | bc -l)
        log_message "Reduced position size to $POSITION_SIZE due to high volatility"
    fi
}

# Function to validate parameter changes using Set Theory
# ↹ parameters•bounds
# ⊕ validate => constraints
# Σ valid•parameters
validate_changes() {
    local current_rsi=$1
    local current_price=$2
    
    # Set Theory: Define valid parameter ranges
    if [ $RSI_PERIOD -lt 5 ] || [ $RSI_PERIOD -gt 50 ]; then
        RSI_PERIOD=14
        log_message "Reset RSI period to default (Set Theory: Valid Range)"
    fi
    
    if [ $OVERBOUGHT -lt 60 ] || [ $OVERBOUGHT -gt 90 ]; then
        OVERBOUGHT=70
        log_message "Reset overbought threshold to default (Set Theory: Valid Range)"
    fi
    
    if [ $OVERSOLD -lt 10 ] || [ $OVERSOLD -gt 40 ]; then
        OVERSOLD=30
        log_message "Reset oversold threshold to default (Set Theory: Valid Range)"
    fi
}

# Main trading loop with mathematical pattern integration
log_message "Starting HFT RSI Strategy with Mathematical Patterns"
log_message "Initial parameters: RSI_PERIOD=$RSI_PERIOD, OVERBOUGHT=$OVERBOUGHT, OVERSOLD=$OVERSOLD"

# Initialize variables using Set Theory
position="NONE"  # Position ∈ {NONE, LONG, SHORT}
entry_price=0
total_pnl=0
total_trades=0
declare -a prices=()

# Trap Ctrl+C to clean up
trap 'echo ""; log_message "Strategy stopped by user"; exit 0' INT

# Function to display status with mathematical patterns
display_status() {
    clear
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║              HFT RSI Strategy with Mathematical Patterns        ║"
    echo "╠════════════════════════════════════════════════════════════════╣"
    echo "║ Set Theory: Parameter Space                                    ║"
    printf "║ • RSI Period ∈ [5,50]: %-41d ║\n" "$RSI_PERIOD"
    printf "║ • Overbought ∈ [60,90]: %-39d ║\n" "$OVERBOUGHT"
    printf "║ • Oversold ∈ [10,40]: %-41d ║\n" "$OVERSOLD"
    echo "╠════════════════════════════════════════════════════════════════╣"
    echo "║ Category Theory: Price Transformations                         ║"
    printf "║ • Current Price: %-45.2f ║\n" "$1"
    if [ "$2" = "N/A" ]; then
        printf "║ • RSI Transform: %-45s ║\n" "$2"
    else
        printf "║ • RSI Transform: %-45.2f ║\n" "$2"
    fi
    printf "║ • Signal Morphism: %-43s ║\n" "$3"
    printf "║ • Position State: %-44s ║\n" "$4"
    echo "╠════════════════════════════════════════════════════════════════╣"
    echo "║ Topology: Performance Measures                                 ║"
    printf "║ • Total P&L: %-47.2f ║\n" "$5"
    printf "║ • Trade Count: %-46d ║\n" "$6"
    
    if [ "$6" -gt 0 ]; then
        metrics=$(calculate_metrics "$5" "$6" "${prices[*]}")
        IFS=',' read -r win_rate sharpe_ratio risk_adjusted_return volatility <<< "$metrics"
        
        printf "║ • Win Rate: %-48.2f%% ║\n" "$(echo "$win_rate * 100" | bc -l)"
        printf "║ • Sharpe Ratio: %-45.2f ║\n" "$sharpe_ratio"
        printf "║ • Risk-Adjusted Return: %-40.2f ║\n" "$risk_adjusted_return"
        printf "║ • Price Volatility: %-43.2f ║\n" "$volatility"
        
        echo "╠════════════════════════════════════════════════════════════════╣"
        echo "║ System Evolution                                               ║"
        local param_changes=$(grep -c "Adjusted" "$LOG_FILE")
        local health_score=$(echo "scale=2; ($win_rate * 0.4 + (1 - $volatility/10) * 0.3 + $risk_adjusted_return * 0.3) * 100" | bc -l)
        printf "║ • Parameter Adaptations: %-39d ║\n" "$param_changes"
        printf "║ • System Health Score: %-41.2f%% ║\n" "$health_score"
        
        if (( $(echo "$health_score > 75" | bc -l) )); then
            echo "║ • Status: Optimal Performance                                  ║"
        elif (( $(echo "$health_score > 50" | bc -l) )); then
            echo "║ • Status: Stable Operation                                    ║"
        elif (( $(echo "$health_score > 25" | bc -l) )); then
            echo "║ • Status: Requires Optimization                               ║"
        else
            echo "║ • Status: Critical - Immediate Adjustment Required            ║"
        fi
    fi
    
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Recent System Events:"
    echo "──────────────────────────────────────────────────────────────────"
    tail -n 5 "$LOG_FILE"
}

# Main loop implementing Category Theory transformations
while true; do
    # Topology: Continuous price evolution
    current_price=$(echo "100 + $(( RANDOM % 100 - 50 )) / 100" | bc -l)
    
    # Display initial status with empty RSI and signal
    if [ ${#prices[@]} -lt $RSI_PERIOD ]; then
        display_status "$current_price" "N/A" "Collecting Data..." "$position" "$total_pnl" "$total_trades"
    fi
    
    # Category Theory: Transform price series
    prices+=($current_price)
    if [ ${#prices[@]} -gt $RSI_PERIOD ]; then
        prices=("${prices[@]:1}")
    fi
    
    # Calculate metrics and make trading decisions
    if [ ${#prices[@]} -eq $RSI_PERIOD ]; then
        rsi=$(calculate_rsi "${prices[*]}")
        signal=$(generate_signal $rsi)
        
        # Trading logic using Category Theory
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
        
        # Calculate P&L using Category Theory
        if [ "$position" != "NONE" ]; then
            local pnl=0
            if [ "$position" == "LONG" ]; then
                pnl=$(echo "$current_price - $entry_price" | bc -l)
            else
                pnl=$(echo "$entry_price - $current_price" | bc -l)
            fi
            total_pnl=$(echo "$total_pnl + $pnl" | bc -l)
            
            # Topology: Continuous monitoring of profit/loss boundaries
            if (( $(echo "$pnl >= $PROFIT_TARGET" | bc -l) )) || (( $(echo "$pnl <= -$STOP_LOSS" | bc -l) )); then
                log_message "Position closed at $current_price (P&L: $pnl)"
                position="NONE"
                entry_price=0
            fi
        fi
        
        # Calculate and log enhanced metrics
        if [ $total_trades -gt 0 ]; then
            metrics=$(calculate_metrics $total_pnl $total_trades "${prices[*]}")
            IFS=',' read -r win_rate sharpe_ratio risk_adjusted_return volatility <<< "$metrics"
            
            # Log to metrics file with enhanced data
            echo "$(date '+%Y-%m-%d %H:%M:%S'),$rsi,$signal,$current_price,$position,$total_pnl,$win_rate,$sharpe_ratio,$risk_adjusted_return,$volatility" >> "$METRICS_FILE"
            
            # Optimize using mathematical patterns
            if (( total_trades % 10 == 0 )); then
                optimize_parameters $win_rate $sharpe_ratio $risk_adjusted_return $volatility
                validate_changes $rsi $current_price
            fi
        fi
    fi
    
    # Sleep with topology-based monitoring message
    for ((i=INTERVAL; i>0; i--)); do
        echo -ne "\r╔═══════════════════════════════════════════════════════════╗"
        echo -ne "\r║ Monitoring Market State - Next Update: $i seconds          ║"
        echo -ne "\r║ Press Ctrl+C to exit                                      ║"
        echo -ne "\r╚═══════════════════════════════════════════════════════════╝\r"
        sleep 1
    done
done
