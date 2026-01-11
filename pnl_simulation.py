"""
Portfolio PnL Simulation Script
Simulates trading performance with 55% win probability
across different position sizing strategies.
"""

import random
import matplotlib.pyplot as plt
import numpy as np

# Simulation parameters
WIN_PROBABILITY = 0.57  # 57% chance of winning
NUM_TRADES = 500        # Number of trades to simulate
NUM_SIMULATIONS = 100   # Number of Monte Carlo simulations per position size
INITIAL_CAPITAL = 10000 # Starting capital

# Position sizes to test (as percentage of portfolio)
POSITION_SIZES = [1, 3, 5, 10, 15, 20, 35]

# Risk/Reward ratio (1:1 means we win what we risk)
RISK_REWARD_RATIO = 1.0


def generate_trade_outcomes(num_trades, win_prob):
    """
    Generate a sequence of trade outcomes (True=win, False=loss).
    All portfolios will use the same sequence for fair comparison.
    """
    return [random.random() < win_prob for _ in range(num_trades)]


def simulate_portfolio(position_size_pct, trade_outcomes, initial_capital, risk_reward=1.0):
    """
    Simulate portfolio performance for a given position size using pre-determined trade outcomes.
    
    Args:
        position_size_pct: Percentage of portfolio to risk per trade (e.g., 5 for 5%)
        trade_outcomes: List of booleans (True=win, False=loss) - SAME for all portfolios
        initial_capital: Starting capital
        risk_reward: Risk/Reward ratio (1.0 = 1:1)
    
    Returns:
        List of portfolio values after each trade
    """
    capital = initial_capital
    portfolio_history = [capital]
    
    for is_win in trade_outcomes:
        if capital <= 0:
            portfolio_history.append(0)
            continue
            
        # Calculate position size in dollars
        risk_amount = capital * (position_size_pct / 100)
        
        # Apply trade outcome (same win/loss for ALL position sizes)
        if is_win:
            # Win: gain risk_amount * risk_reward
            capital += risk_amount * risk_reward
        else:
            # Loss: lose risk_amount
            capital -= risk_amount
        
        portfolio_history.append(max(0, capital))
    
    return portfolio_history


def run_monte_carlo(position_sizes, num_simulations, num_trades, win_prob, initial_capital, risk_reward=1.0):
    """
    Run multiple simulations where ALL position sizes share the SAME trade outcomes.
    
    Returns:
        Dict of position_size -> list of simulation results
    """
    all_results = {pos: [] for pos in position_sizes}
    
    for sim_num in range(num_simulations):
        # Generate ONE sequence of trades - ALL position sizes use this SAME sequence
        trade_outcomes = generate_trade_outcomes(num_trades, win_prob)
        
        # Apply the same trades to each position size strategy
        for pos_size in position_sizes:
            history = simulate_portfolio(pos_size, trade_outcomes, initial_capital, risk_reward)
            all_results[pos_size].append(history)
    
    return all_results


def calculate_statistics(simulations, initial_capital):
    """
    Calculate statistics from simulation results.
    """
    final_values = [sim[-1] for sim in simulations]
    
    stats = {
        'mean_final': np.mean(final_values),
        'median_final': np.median(final_values),
        'std_final': np.std(final_values),
        'min_final': np.min(final_values),
        'max_final': np.max(final_values),
        'profitable_pct': sum(1 for v in final_values if v > initial_capital) / len(final_values) * 100,
        'bankrupt_pct': sum(1 for v in final_values if v <= 0) / len(final_values) * 100,
        'mean_return_pct': ((np.mean(final_values) - initial_capital) / initial_capital) * 100,
        'median_return_pct': ((np.median(final_values) - initial_capital) / initial_capital) * 100,
    }
    return stats


def main():
    print("=" * 70)
    print("PORTFOLIO PnL SIMULATION")
    print("=" * 70)
    print(f"\nSimulation Parameters:")
    print(f"  - Win Probability: {WIN_PROBABILITY * 100}%")
    print(f"  - Number of Trades: {NUM_TRADES}")
    print(f"  - Monte Carlo Simulations: {NUM_SIMULATIONS}")
    print(f"  - Initial Capital: ${INITIAL_CAPITAL:,.2f}")
    print(f"  - Risk/Reward Ratio: 1:{RISK_REWARD_RATIO}")
    print(f"  - Position Sizes: {POSITION_SIZES}%")
    print(f"\n  *** ALL position sizes participate in the SAME trades! ***")
    print("\n" + "=" * 70)
    
    # Store results for each position size
    all_stats = {}
    
    # Run simulations - ALL position sizes share the SAME trade sequences
    print(f"\nRunning {NUM_SIMULATIONS} simulations (all position sizes trade together)...")
    all_results = run_monte_carlo(
        POSITION_SIZES, NUM_SIMULATIONS, NUM_TRADES,
        WIN_PROBABILITY, INITIAL_CAPITAL, RISK_REWARD_RATIO
    )
    
    # Calculate statistics for each position size
    for pos_size in POSITION_SIZES:
        all_stats[pos_size] = calculate_statistics(all_results[pos_size], INITIAL_CAPITAL)
    
    # Print statistics table
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print(f"\n{'Position':<10} {'Mean Final':<15} {'Median Final':<15} {'Mean Return':<12} {'Profitable':<12} {'Bankrupt':<10}")
    print(f"{'Size %':<10} {'Capital ($)':<15} {'Capital ($)':<15} {'(%)':<12} {'(%)':<12} {'(%)':<10}")
    print("-" * 70)
    
    for pos_size in POSITION_SIZES:
        stats = all_stats[pos_size]
        print(f"{pos_size:<10} {stats['mean_final']:>14,.0f} {stats['median_final']:>14,.0f} "
              f"{stats['mean_return_pct']:>11.1f} {stats['profitable_pct']:>11.1f} {stats['bankrupt_pct']:>9.1f}")
    
    # Additional detailed statistics
    print("\n" + "=" * 70)
    print("DETAILED STATISTICS")
    print("=" * 70)
    
    for pos_size in POSITION_SIZES:
        stats = all_stats[pos_size]
        print(f"\n{pos_size}% Position Size:")
        print(f"  Min Final Capital:  ${stats['min_final']:>15,.2f}")
        print(f"  Max Final Capital:  ${stats['max_final']:>15,.2f}")
        print(f"  Std Deviation:      ${stats['std_final']:>15,.2f}")
    
    # Create visualization
    
    # Define distinct colors for better differentiation
    COLORS = {
        1: '#2ecc71',    # Green
        3: '#3498db',    # Blue  
        5: '#9b59b6',    # Purple
        10: '#f39c12',   # Orange
        15: '#e74c3c',   # Red
        20: '#1abc9c',   # Teal
        35: '#e91e63',   # Pink
    }
    
    # FIGURE 1: Dedicated Equity Curves Chart (larger, more detailed)
    fig1, ax_eq = plt.subplots(figsize=(14, 8))
    
    for pos_size in POSITION_SIZES:
        # Plot median simulation
        median_idx = np.argsort([sim[-1] for sim in all_results[pos_size]])[NUM_SIMULATIONS // 2]
        ax_eq.plot(all_results[pos_size][median_idx], label=f'{pos_size}%', color=COLORS[pos_size], alpha=0.9, linewidth=2.5)
    
    ax_eq.axhline(y=INITIAL_CAPITAL, color='black', linestyle='--', alpha=0.5, linewidth=1.5, label='Initial Capital')
    ax_eq.set_xlabel('Trade Number', fontsize=12)
    ax_eq.set_ylabel('Portfolio Value ($)', fontsize=12)
    ax_eq.set_title('Equity Curves by Position Size (Median Simulation)\nAll portfolios trade the SAME sequence', fontsize=14)
    ax_eq.legend(loc='upper left', fontsize=11)
    ax_eq.set_yscale('log')
    ax_eq.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('equity_curves.png', dpi=150, bbox_inches='tight')
    
    # FIGURE 2: Other statistics charts
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Sample equity curves (smaller version)
    ax1 = axes[0, 0]
    for pos_size in POSITION_SIZES:
        median_idx = np.argsort([sim[-1] for sim in all_results[pos_size]])[NUM_SIMULATIONS // 2]
        ax1.plot(all_results[pos_size][median_idx], label=f'{pos_size}%', color=COLORS[pos_size], alpha=0.9, linewidth=2)
    
    ax1.axhline(y=INITIAL_CAPITAL, color='black', linestyle='--', alpha=0.5, label='Initial Capital')
    ax1.set_xlabel('Trade Number')
    ax1.set_ylabel('Portfolio Value ($)')
    ax1.set_title('Median Equity Curves by Position Size')
    ax1.legend(loc='upper left')
    ax1.set_yscale('log')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Final capital distribution (box plot)
    ax2 = axes[0, 1]
    final_values_list = [[sim[-1] for sim in all_results[pos]] for pos in POSITION_SIZES]
    bp = ax2.boxplot(final_values_list, labels=[f'{p}%' for p in POSITION_SIZES], patch_artist=True)
    
    for pos_size, patch in zip(POSITION_SIZES, bp['boxes']):
        patch.set_facecolor(COLORS[pos_size])
        patch.set_alpha(0.7)
    
    ax2.axhline(y=INITIAL_CAPITAL, color='red', linestyle='--', alpha=0.5, label='Initial Capital')
    ax2.set_xlabel('Position Size')
    ax2.set_ylabel('Final Portfolio Value ($)')
    ax2.set_title('Final Capital Distribution by Position Size')
    ax2.set_yscale('log')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Mean and Median returns
    ax3 = axes[1, 0]
    mean_returns = [all_stats[p]['mean_return_pct'] for p in POSITION_SIZES]
    median_returns = [all_stats[p]['median_return_pct'] for p in POSITION_SIZES]
    
    x = np.arange(len(POSITION_SIZES))
    width = 0.35
    
    bars1 = ax3.bar(x - width/2, mean_returns, width, label='Mean Return', color='steelblue', alpha=0.8)
    bars2 = ax3.bar(x + width/2, median_returns, width, label='Median Return', color='coral', alpha=0.8)
    
    ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax3.set_xlabel('Position Size')
    ax3.set_ylabel('Return (%)')
    ax3.set_title('Mean vs Median Returns by Position Size')
    ax3.set_xticks(x)
    ax3.set_xticklabels([f'{p}%' for p in POSITION_SIZES])
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Plot 4: Risk metrics (profitable % and bankrupt %)
    ax4 = axes[1, 1]
    profitable_pcts = [all_stats[p]['profitable_pct'] for p in POSITION_SIZES]
    bankrupt_pcts = [all_stats[p]['bankrupt_pct'] for p in POSITION_SIZES]
    
    ax4.bar(x - width/2, profitable_pcts, width, label='Profitable %', color='green', alpha=0.7)
    ax4.bar(x + width/2, bankrupt_pcts, width, label='Bankrupt %', color='red', alpha=0.7)
    
    ax4.set_xlabel('Position Size')
    ax4.set_ylabel('Percentage of Simulations')
    ax4.set_title('Probability of Profit vs Bankruptcy')
    ax4.set_xticks(x)
    ax4.set_xticklabels([f'{p}%' for p in POSITION_SIZES])
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.set_ylim(0, 100)
    
    plt.tight_layout()
    plt.savefig('position_sizing_simulation.png', dpi=150, bbox_inches='tight')
    print("\n" + "=" * 70)
    print("Charts saved:")
    print("  - 'equity_curves.png' (detailed equity curves)")
    print("  - 'position_sizing_simulation.png' (all statistics)")
    plt.show()
    
    # Print key insights
    print("\n" + "=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print("""
    1. POSITION SIZING MATTERS: Even with a positive edge (55% win rate),
       oversized positions can lead to ruin due to variance.
    
    2. OPTIMAL KELLY CRITERION: For a 55% win rate with 1:1 R:R,
       Kelly suggests betting ~10% (2*0.55 - 1 = 0.10), but this is
       considered aggressive. Many traders use "Half Kelly" (5%).
    
    3. RISK OF RUIN: Larger position sizes dramatically increase the
       chance of significant drawdowns or complete account blowup.
    
    4. MEDIAN vs MEAN: The mean can be misleading due to outliers.
       Focus on median returns for realistic expectations.
    
    5. CONSERVATIVE SIZING: 1-3% position sizing provides more
       consistent growth with lower risk of catastrophic losses.
    """)


if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    np.random.seed(42)
    main()
