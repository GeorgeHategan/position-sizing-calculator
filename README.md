# Position Sizing Calculator

A comprehensive Monte Carlo simulation toolkit for analyzing optimal position sizing strategies in trading. These tools help traders determine the ideal percentage of their portfolio to risk per trade based on their win rate and risk/reward ratio.

## 🎯 Purpose

Position sizing is one of the most critical aspects of trading risk management. Risking too little leads to underwhelming returns, while risking too much can lead to catastrophic losses or complete account bankruptcy. This repository provides two powerful simulation tools to help traders:

1. **Find the optimal position size** for their specific trading strategy
2. **Compare multiple position sizing strategies** side-by-side
3. **Understand risk-return tradeoffs** through comprehensive metrics
4. **Avoid common position sizing mistakes** that lead to account ruin

## 📊 What's Included

### 1. `optimal_position_finder.py`
The comprehensive tool for finding your optimal position size through pure Monte Carlo simulation.

**Key Features:**
- Tests position sizes from 1% to 40% in 0.5% increments (80 different sizes)
- Runs 500 Monte Carlo simulations per position size
- Provides multiple optimization criteria:
  - **Best Geometric Mean Return** (most realistic long-term growth)
  - **Best Median Return** (typical outcome)
  - **Best Risk-Adjusted Return** (Sharpe-like ratio)
  - **Best Safe Growth** (< 30% drawdown)
  - **Best Very Safe Growth** (< 20% drawdown)

**Performance Metrics:**
- Mean, median, and geometric mean returns
- Standard deviation and volatility
- Maximum drawdown analysis
- Bankruptcy probability
- Profitability percentage
- Sharpe-like risk-adjusted returns

**Output:**
- Detailed statistics table for all position sizes
- Optimal position size recommendations based on different criteria
- Visual chart showing key metrics across position sizes

### 2. `pnl_simulation.py`
A comparative tool that simulates multiple position sizing strategies simultaneously using identical trade sequences.

**Key Features:**
- Compares predefined position sizes (1%, 3%, 5%, 10%, 15%, 20%, 35%)
- 100 Monte Carlo simulations
- All position sizes experience the **same** trades for fair comparison
- Generates equity curve visualizations

**Performance Metrics:**
- Mean and median final capital
- Mean and median return percentages
- Profitability percentage
- Bankruptcy rate
- Min/max outcomes

**Output:**
- Comparative statistics table
- Equity curve charts showing portfolio growth over time
- Visual comparison of different position sizing strategies

## 🔧 Default Parameters

Both tools are pre-configured with the following parameters (easily customizable in the code):

- **Win Probability:** 57% (a typical edge for profitable traders)
- **Risk/Reward Ratio:** 1:1 (win amount equals risk amount)
- **Number of Trades:** 500 (simulates 500 trades per simulation)
- **Initial Capital:** $10,000
- **Monte Carlo Simulations:** 100-500 (depending on the tool)

## 🚀 Usage

### Prerequisites
```bash
pip install numpy matplotlib
```

### Running the Optimal Position Finder
```bash
python optimal_position_finder.py
```

This will:
1. Run comprehensive simulations across 80 different position sizes
2. Print detailed performance metrics for each position size
3. Display optimal recommendations based on various criteria
4. Generate a visualization chart

### Running the PnL Simulation
```bash
python pnl_simulation.py
```

This will:
1. Simulate trading performance across predefined position sizes
2. Print comparative statistics
3. Generate equity curve visualizations showing portfolio growth

## 📈 Sample Output

### Position Finder Recommendations
```
OPTIMAL POSITION SIZES (from simulation):
  - Best Geometric Mean Return: 8.5%
  - Best Median Return: 9.0%
  - Best Risk-Adjusted (Sharpe): 7.5%
  - Best Safe Growth (<30% DD): 6.5%
  - Best Very Safe (<20% DD): 4.5%
```

### PnL Simulation Results
```
Position    Mean Final      Median Final    Mean Return  Profitable   Bankrupt
Size %      Capital ($)     Capital ($)     (%)          (%)          (%)
----------------------------------------------------------------------
1           12,450          12,380          24.5         95.0         0.0
5           18,920          16,240          89.2         87.0         0.5
10          24,580          18,950          145.8        78.0         3.2
20          31,240          12,460          212.4        65.0         15.8
```

## 📊 Generated Visualizations

The tools generate PNG charts showing:
- **Equity Curves:** Portfolio value progression over 500 trades
- **Position Size Comparison:** Multiple metrics plotted against position size
- **Risk-Return Analysis:** Visualizing the tradeoff between returns and risk

## ⚙️ Customization

You can easily modify the simulation parameters at the top of each file:

```python
WIN_PROBABILITY = 0.57     # Your strategy's win rate
RISK_REWARD_RATIO = 1.5    # Your typical risk/reward ratio
NUM_TRADES = 500           # Number of trades to simulate
INITIAL_CAPITAL = 10000    # Starting capital
```

## 🎓 Key Insights

### Why Not Just Use Kelly Criterion?

While the Kelly Criterion provides a mathematical formula for optimal position sizing, these simulation tools offer several advantages:

1. **Visual Understanding:** See exactly how different position sizes perform
2. **Multiple Metrics:** Optimize for geometric mean, median, or risk-adjusted returns
3. **Risk Analysis:** Understand drawdown and bankruptcy probabilities
4. **Real-World Scenarios:** Monte Carlo simulations capture the randomness of actual trading
5. **Conservative Options:** Find position sizes that balance growth with safety

### Common Findings

- **Optimal position sizes** are typically much smaller than traders expect (usually 4-12%)
- **Geometric mean return** is the best metric for long-term growth
- **Large position sizes** (>20%) often lead to significant bankruptcy risk even with a 57% win rate
- **Risk-adjusted optimal** is often smaller than return-maximizing optimal

## 📝 Use Cases

- **Strategy Development:** Determine appropriate position sizing for a new trading strategy
- **Risk Management:** Understand the relationship between position size and account risk
- **Backtesting Enhancement:** Add realistic position sizing to your backtest results
- **Education:** Learn how position sizing impacts long-term trading success
- **Portfolio Optimization:** Find the sweet spot between growth and capital preservation

## ⚠️ Disclaimer

These tools are for educational and research purposes. Past performance and simulated results do not guarantee future results. Always practice proper risk management and never risk more than you can afford to lose.

## 🤝 Contributing

Feel free to open issues or submit pull requests with improvements, additional metrics, or new features.

## 📄 License

MIT License - feel free to use and modify for your own trading research.

---

**Happy Trading! 📈**
