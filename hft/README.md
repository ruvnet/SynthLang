
# High Frequency Trading RSI Strategy

This directory contains an implementation of a high-frequency trading strategy using the Relative Strength Index (RSI) with self-learning capabilities.

## Files

- `hft_rsi_strategy.md` - Detailed specification of the trading strategy
- `hft_rsi_strategy.sh` - Bash implementation of the strategy with self-learning

## Requirements

- Bash shell environment
- `bc` command-line calculator
- Sufficient permissions to create directories and files

## Usage

1. Make sure the script is executable:
```bash
chmod +x hft_rsi_strategy.sh
```

2. Run the strategy:
```bash
./hft_rsi_strategy.sh
```

The script will:
- Create necessary directories (data, logs, metrics)
- Initialize logging and metrics collection
- Start the trading loop with 1-minute intervals
- Automatically optimize parameters based on performance
- Log all activities and metrics

## Directory Structure

```
hft/
├── data/           # Directory for market data
├── logs/           # Trading logs
│   └── trading_YYYYMMDD.log
└── metrics/        # Performance metrics
    └── performance_YYYYMMDD.csv
```

## Metrics and Monitoring

The strategy tracks several key metrics:
- RSI values
- Trading signals
- Position status
- Profit/Loss (PnL)
- Win rate
- Sharpe ratio

These metrics are saved in CSV format in the metrics directory.

## Self-Learning Features

The strategy includes:
- Automatic parameter optimization based on performance
- Dynamic adjustment of RSI period
- Adaptive overbought/oversold thresholds
- Parameter validation to prevent extreme values
- Performance-based learning cycles every 10 trades

## Stopping the Strategy

Press Ctrl+C to gracefully stop the strategy. This will:
- Log the final state
- Save all metrics
- Clean up resources

## Logs and Analysis

1. View real-time logs:
```bash
tail -f logs/trading_YYYYMMDD.log
```

2. Analyze performance metrics:
```bash
cat metrics/performance_YYYYMMDD.csv
```

## Important Notes

- This is a simulation using random price data
- For real trading, replace the price generation with actual market data
- Adjust parameters (RSI_PERIOD, OVERBOUGHT, OVERSOLD) based on your market
- Monitor system resources when running for extended periods
- Always paper trade first before using real funds

## Risk Warning

This is a demonstration implementation. Real trading requires:
- Proper risk management
- Real market data integration
- Additional safety checks
- Thorough testing
- Regulatory compliance
- Professional oversight

## Next Steps

1. Integrate real market data
2. Add more sophisticated risk management
3. Implement additional technical indicators
4. Enhance the self-learning mechanism
5. Add real-time monitoring dashboard
6. Implement emergency shutdown procedures
