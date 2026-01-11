"""
Optimal Position Size Finder (PURE SIMULATION)
Tests many position sizes to find the optimal one for a 55% win rate strategy.
NO Kelly formula - finds optimal purely through Monte Carlo simulation.
"""

import random
import matplotlib.pyplot as plt
import numpy as np

# Simulation parameters
WIN_PROBABILITY = 0.57  # 57% chance of winning
NUM_TRADES = 500        # Number of trades to simulate
NUM_SIMULATIONS = 500   # Number of Monte Carlo simulations (more = better accuracy)
INITIAL_CAPITAL = 10000 # Starting capital
RISK_REWARD_RATIO = 1.0 # 1:1 risk/reward

# Test position sizes from 1% to 40% in 0.5% increments for precision
POSITION_SIZES = [x / 2 for x in range(2, 81)]  # 1%, 1.5%, 2%, ... 40%


def generate_trade_outcomes(num_trades, win_prob):
    """Generate a sequence of trade outcomes (True=win, False=loss)."""
    return [random.random() < win_prob for _ in range(num_trades)]


def simulate_portfolio(position_size_pct, trade_outcomes, initial_capital, risk_reward=1.0):
    """Simulate portfolio performance for a given position size."""
    capital = initial_capital
    portfolio_history = [capital]
    max_drawdown = 0
    peak = capital
    
    for is_win in trade_outcomes:
        if capital <= 0:
            portfolio_history.append(0)
            continue
            
        risk_amount = capital * (position_size_pct / 100)
        
        if is_win:
            capital += risk_amount * risk_reward
        else:
            capital -= risk_amount
        
        capital = max(0, capital)
        portfolio_history.append(capital)
        
        # Track drawdown
        if capital > peak:
            peak = capital
        drawdown = (peak - capital) / peak if peak > 0 else 0
        max_drawdown = max(max_drawdown, drawdown)
    
    return portfolio_history, max_drawdown


def run_simulations(position_sizes, num_simulations, num_trades, win_prob, initial_capital, risk_reward=1.0):
    """Run Monte Carlo simulations for all position sizes."""
    results = {pos: {'final_values': [], 'max_drawdowns': [], 'histories': []} for pos in position_sizes}
    
    print(f"  Running {num_simulations} simulations...")
    for sim_num in range(num_simulations):
        if (sim_num + 1) % 100 == 0:
            print(f"    Simulation {sim_num + 1}/{num_simulations}")
        
        # Same trade sequence for all position sizes
        trade_outcomes = generate_trade_outcomes(num_trades, win_prob)
        
        for pos_size in position_sizes:
            history, max_dd = simulate_portfolio(pos_size, trade_outcomes, initial_capital, risk_reward)
            results[pos_size]['final_values'].append(history[-1])
            results[pos_size]['max_drawdowns'].append(max_dd)
            results[pos_size]['histories'].append(history)
    
    return results


def calculate_metrics(results, initial_capital):
    """Calculate performance metrics for each position size."""
    metrics = {}
    
    for pos_size, data in results.items():
        final_values = data['final_values']
        max_drawdowns = data['max_drawdowns']
        
        # Calculate geometric mean return (CAGR proxy) - THE KEY METRIC
        returns = [(fv / initial_capital) for fv in final_values]
        geo_mean_return = np.exp(np.mean(np.log([max(r, 0.0001) for r in returns]))) - 1
        
        metrics[pos_size] = {
            'mean_final': np.mean(final_values),
            'median_final': np.median(final_values),
            'geo_mean_return': geo_mean_return * 100,
            'mean_return': (np.mean(final_values) / initial_capital - 1) * 100,
            'median_return': (np.median(final_values) / initial_capital - 1) * 100,
            'std_final': np.std(final_values),
            'avg_max_drawdown': np.mean(max_drawdowns) * 100,
            'worst_drawdown': np.max(max_drawdowns) * 100,
            'profitable_pct': sum(1 for v in final_values if v > initial_capital) / len(final_values) * 100,
            'bankrupt_pct': sum(1 for v in final_values if v <= 0) / len(final_values) * 100,
            'sharpe_like': (np.mean(final_values) - initial_capital) / np.std(final_values) if np.std(final_values) > 0 else 0,
        }
    
    return metrics


def find_optimal_sizes(metrics):
    """Find optimal position sizes based on different criteria - ALL FROM SIMULATION."""
    pos_sizes = list(metrics.keys())
    
    # Best by geometric mean return (most realistic long-term growth)
    best_geo = max(pos_sizes, key=lambda x: metrics[x]['geo_mean_return'])
    
    # Best by median final value
    best_median = max(pos_sizes, key=lambda x: metrics[x]['median_final'])
    
    # Best by mean final value  
    best_mean = max(pos_sizes, key=lambda x: metrics[x]['mean_final'])
    
    # Best risk-adjusted (highest Sharpe-like ratio)
    best_sharpe = max(pos_sizes, key=lambda x: metrics[x]['sharpe_like'])
    
    # Best with max drawdown < 30%
    safe_sizes = [p for p in pos_sizes if metrics[p]['avg_max_drawdown'] < 30]
    best_safe = max(safe_sizes, key=lambda x: metrics[x]['geo_mean_return']) if safe_sizes else None
    
    # Best with max drawdown < 20% (very conservative)
    very_safe = [p for p in pos_sizes if metrics[p]['avg_max_drawdown'] < 20]
    best_very_safe = max(very_safe, key=lambda x: metrics[x]['geo_mean_return']) if very_safe else None
    
    return {
        'best_geometric': best_geo,
        'best_median': best_median,
        'best_mean': best_mean,
        'best_risk_adjusted': best_sharpe,
        'best_safe_growth': best_safe,
        'best_very_safe': best_very_safe,
    }


def main():
    print("=" * 70)
    print("OPTIMAL POSITION SIZE FINDER (PURE SIMULATION)")
    print("=" * 70)
    print(f"\nParameters:")
    print(f"  - Win Probability: {WIN_PROBABILITY * 100}%")
    print(f"  - Risk/Reward Ratio: 1:{RISK_REWARD_RATIO}")
    print(f"  - Number of Trades: {NUM_TRADES}")
    print(f"  - Monte Carlo Simulations: {NUM_SIMULATIONS}")
    print(f"  - Initial Capital: ${INITIAL_CAPITAL:,.2f}")
    print(f"  - Testing Position Sizes: {min(POSITION_SIZES)}% to {max(POSITION_SIZES)}%")
    print(f"\n  ** NO KELLY FORMULA - Finding optimal through simulation only! **")
    
    print("\n" + "=" * 70)
    
    # Run simulations
    results = run_simulations(
        POSITION_SIZES, NUM_SIMULATIONS, NUM_TRADES,
        WIN_PROBABILITY, INITIAL_CAPITAL, RISK_REWARD_RATIO
    )
    
    # Calculate metrics
    metrics = calculate_metrics(results, INITIAL_CAPITAL)
    
    # Find optimal sizes (ALL FROM SIMULATION)
    optimal = find_optimal_sizes(metrics)
    
    # Print results
    print("\n" + "=" * 70)
    print("SIMULATION RESULTS - OPTIMAL POSITION SIZES")
    print("=" * 70)
    print(f"\n  *** ALL VALUES DERIVED FROM SIMULATION - NO FORMULA ***")
    print(f"\n  OPTIMAL POSITION SIZE (Best Geometric Growth): {optimal['best_geometric']}%")
    print(f"\n  Other Criteria:")
    print(f"  - Best Median Return:            {optimal['best_median']}%")
    print(f"  - Best Mean Return:              {optimal['best_mean']}%")
    print(f"  - Best Risk-Adjusted:            {optimal['best_risk_adjusted']}%")
    if optimal['best_safe_growth']:
        print(f"  - Best Safe Growth (<30% DD):    {optimal['best_safe_growth']}%")
    if optimal['best_very_safe']:
        print(f"  - Best Very Safe (<20% DD):      {optimal['best_very_safe']}%")
    
    # Show metrics for the optimal size
    opt = optimal['best_geometric']
    print(f"\n  Metrics for OPTIMAL {opt}% position size:")
    print(f"    - Geometric Return:    {metrics[opt]['geo_mean_return']:.1f}%")
    print(f"    - Median Return:       {metrics[opt]['median_return']:.1f}%")
    print(f"    - Avg Max Drawdown:    {metrics[opt]['avg_max_drawdown']:.1f}%")
    print(f"    - Profitable:          {metrics[opt]['profitable_pct']:.1f}%")
    print(f"    - Bankrupt:            {metrics[opt]['bankrupt_pct']:.1f}%")
    
    # Detailed metrics table (show key sizes)
    print("\n" + "=" * 70)
    print("DETAILED METRICS BY POSITION SIZE")
    print("=" * 70)
    print(f"\n{'Size':<6} {'Geo Return':<12} {'Median Ret':<12} {'Avg MaxDD':<10} {'Profitable':<11} {'Bankrupt':<9}")
    print(f"{'(%)':<6} {'(%)':<12} {'(%)':<12} {'(%)':<10} {'(%)':<11} {'(%)':<9}")
    print("-" * 70)
    
    # Show every 1% increment for clarity
    key_sizes = [p for p in POSITION_SIZES if p == int(p) or p == optimal['best_geometric']]
    for pos_size in sorted(set(key_sizes)):
        m = metrics[pos_size]
        marker = " <-- OPTIMAL" if pos_size == optimal['best_geometric'] else ""
        print(f"{pos_size:<6} {m['geo_mean_return']:>11.1f} {m['median_return']:>11.1f} "
              f"{m['avg_max_drawdown']:>9.1f} {m['profitable_pct']:>10.1f} {m['bankrupt_pct']:>8.1f}{marker}")
    
    # Create visualization
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    pos_list = list(POSITION_SIZES)
    opt_size = optimal['best_geometric']
    
    # Plot 1: Returns by position size
    ax1 = axes[0, 0]
    geo_returns = [metrics[p]['geo_mean_return'] for p in pos_list]
    median_returns = [metrics[p]['median_return'] for p in pos_list]
    
    ax1.plot(pos_list, geo_returns, 'b-', linewidth=2, label='Geometric Mean Return', marker='', markersize=4)
    ax1.plot(pos_list, median_returns, 'g--', linewidth=2, label='Median Return', marker='', markersize=4)
    ax1.axvline(x=opt_size, color='red', linestyle='-', linewidth=2, label=f'OPTIMAL ({opt_size}%)')
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax1.set_xlabel('Position Size (%)', fontsize=11)
    ax1.set_ylabel('Return (%)', fontsize=11)
    ax1.set_title('Returns vs Position Size (FROM SIMULATION)', fontsize=12)
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Risk metrics
    ax2 = axes[0, 1]
    avg_dd = [metrics[p]['avg_max_drawdown'] for p in pos_list]
    worst_dd = [metrics[p]['worst_drawdown'] for p in pos_list]
    
    ax2.plot(pos_list, avg_dd, 'r-', linewidth=2, label='Avg Max Drawdown', marker='', markersize=4)
    ax2.plot(pos_list, worst_dd, 'darkred', linestyle='--', linewidth=2, label='Worst Drawdown', marker='', markersize=4)
    ax2.axvline(x=opt_size, color='blue', linestyle='-', linewidth=2, label=f'OPTIMAL ({opt_size}%)')
    ax2.set_xlabel('Position Size (%)', fontsize=11)
    ax2.set_ylabel('Drawdown (%)', fontsize=11)
    ax2.set_title('Drawdown Risk vs Position Size', fontsize=12)
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Profitable vs Bankrupt %
    ax3 = axes[1, 0]
    profitable = [metrics[p]['profitable_pct'] for p in pos_list]
    bankrupt = [metrics[p]['bankrupt_pct'] for p in pos_list]
    
    ax3.plot(pos_list, profitable, 'g-', linewidth=2, label='Profitable %', marker='', markersize=4)
    ax3.plot(pos_list, bankrupt, 'r-', linewidth=2, label='Bankrupt %', marker='', markersize=4)
    ax3.axvline(x=opt_size, color='blue', linestyle='-', linewidth=2, label=f'OPTIMAL ({opt_size}%)')
    ax3.set_xlabel('Position Size (%)', fontsize=11)
    ax3.set_ylabel('Percentage of Simulations', fontsize=11)
    ax3.set_title('Probability of Profit vs Bankruptcy', fontsize=12)
    ax3.legend(loc='best')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Risk-adjusted returns (Sharpe-like)
    ax4 = axes[1, 1]
    sharpe = [metrics[p]['sharpe_like'] for p in pos_list]
    
    ax4.plot(pos_list, sharpe, 'purple', linewidth=2, label='Risk-Adjusted Score', marker='', markersize=4)
    ax4.axvline(x=opt_size, color='blue', linestyle='-', linewidth=2, label=f'OPTIMAL ({opt_size}%)')
    ax4.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax4.set_xlabel('Position Size (%)', fontsize=11)
    ax4.set_ylabel('Risk-Adjusted Score', fontsize=11)
    ax4.set_title('Risk-Adjusted Performance vs Position Size', fontsize=12)
    ax4.legend(loc='best')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('optimal_position_size.png', dpi=150, bbox_inches='tight')
    
    print("\n" + "=" * 70)
    print("Chart saved to 'optimal_position_size.png'")
    
    # Key insights
    print("\n" + "=" * 70)
    print("CONCLUSION (FROM PURE SIMULATION)")
    print("=" * 70)
    print(f"""
    For a {WIN_PROBABILITY*100}% win rate with {RISK_REWARD_RATIO}:1 Risk/Reward:
    
    ************************************************************
    *  OPTIMAL POSITION SIZE = {opt_size}%  (from simulation)   
    ************************************************************
    
    This was found by simulating {NUM_SIMULATIONS} different random 
    trade sequences of {NUM_TRADES} trades each, and measuring which 
    position size produced the best geometric (compounded) growth.
    
    No formula was used - this is pure empirical testing!
    """)
    
    plt.show()


if __name__ == "__main__":
    random.seed(42)
    np.random.seed(42)
    main()
