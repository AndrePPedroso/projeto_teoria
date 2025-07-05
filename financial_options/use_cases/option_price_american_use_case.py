import numpy as np
import matplotlib.pyplot as plt
import io
import base64

def american_option_lsmc(S0, K, T, r, sigma, num_simulacoes, num_passos, option_type='put'):
    """
    Calculates the price of an American option using the Least Squares Monte Carlo method.

    Args:
        S0 (float): Initial stock price.
        K (float): Strike price.
        T (float): Time to maturity in years.
        r (float): Risk-free interest rate (annual).
        sigma (float): Volatility of the underlying asset (annual).
        num_simulacoes (int): Number of simulated price paths.
        num_passos (int): Number of time steps for the simulation.
        option_type (str): Type of the option, 'put' or 'call'.

    Returns:
        tuple: A tuple containing:
            - float: The estimated price of the American option.
            - numpy.ndarray: The matrix of simulated stock prices.
            - numpy.ndarray: The optimal exercise boundary.
    """
    dt = T / num_passos
    # Convert percentage rates to decimal
    r_dec = r / 100.0
    sigma_dec = sigma / 100.0

    # Generate stock price paths using Geometric Brownian Motion
    S = np.zeros((num_passos + 1, num_simulacoes))
    S[0] = S0
    for t in range(1, num_passos + 1):
        z = np.random.standard_normal(num_simulacoes)
        S[t] = S[t - 1] * np.exp((r_dec - 0.5 * sigma_dec**2) * dt + sigma_dec * np.sqrt(dt) * z)

    # Calculate payoff at maturity based on option type
    if option_type == 'put':
        payoff = np.maximum(K - S, 0)
    else: # 'call'
        payoff = np.maximum(S - K, 0)

    cash_flow = payoff[-1]
    exercise_boundary = np.full(num_passos + 1, np.nan)
    exercise_boundary[-1] = K

    # Backward induction (Longstaff-Schwartz algorithm)
    for t in range(num_passos - 1, 0, -1):
        # Discount future cash flows to the current time step
        discount_factor = np.exp(-r_dec * dt)
        cash_flow = cash_flow * discount_factor
        
        # Identify paths where the option is in-the-money
        in_the_money_paths = payoff[t] > 0
        # If there are no in-the-money paths, there's no possibility of early exercise
        if not np.any(in_the_money_paths):
            continue
        # Perform regression only on in-the-money paths
        X = S[t, in_the_money_paths]
        Y = cash_flow[in_the_money_paths]
        
        # Regress discounted future cash flows on stock prices
        # Using a polynomial of degree 2 as basis functions: 1, x, x^2
        regression_coeffs = np.polyfit(X, Y, 2)
        
        # Estimate the continuation value (expected future payoff if not exercised)
        continuation_value = np.polyval(regression_coeffs, X)
        
        # Find the exercise boundary (where immediate exercise value equals continuation value)
        # This is a heuristic for visualization and is not part of the pricing itself
        try:
            if option_type == 'put':
                # For a put: K - x = ax^2 + bx + c  => ax^2 + (b+1)x + (c-K) = 0
                poly_coeffs = [regression_coeffs[0], regression_coeffs[1] + 1, regression_coeffs[2] - K]
            else: # For a call: x - K = ax^2 + bx + c => ax^2 + (b-1)x + (c+K) = 0
                poly_coeffs = [regression_coeffs[0], regression_coeffs[1] - 1, regression_coeffs[2] + K]
            
            roots = np.roots(poly_coeffs)
            real_roots = roots[np.isreal(roots)].real
            # Heuristic to choose the correct boundary root from the polynomial's solutions
            boundary_candidate = real_roots[(real_roots > 0) & (real_roots < S0 * 2) & (real_roots > S0/2)]
            if len(boundary_candidate) > 0:
                exercise_boundary[t] = np.min(boundary_candidate) if option_type == 'put' else np.max(boundary_candidate)
        except np.linalg.LinAlgError:
            # In some cases, the polynomial fit might be degenerate; we can ignore the boundary calculation
            pass

        # Decide whether to exercise early
        # Compare immediate exercise payoff with the estimated continuation value
        exercise_now_mask = payoff[t, in_the_money_paths] > continuation_value
        
        # Get indices of paths where early exercise is optimal
        exercise_indices = np.where(in_the_money_paths)[0][exercise_now_mask]
        
        # Update cash flows: if exercised, the cash flow is the immediate payoff
        cash_flow[exercise_indices] = payoff[t, exercise_indices]

    # The option price is the discounted average of the cash flows at the first step
    option_price = np.mean(cash_flow * np.exp(-r_dec * dt))
    
    return option_price, S, exercise_boundary


def create_american_option_plots(S, exercise_boundary, option_type, num_simulacoes, num_paths_to_plot=50):
    """
    Creates plots for the American option simulation.

    Args:
        S (numpy.ndarray): Matrix of simulated stock prices.
        exercise_boundary (numpy.ndarray): The optimal exercise boundary.
        option_type (str): The type of option ('put' or 'call').
        num_simulacoes (int): The total number of simulations.
        num_paths_to_plot (int): Number of price paths to display on the plot.

    Returns:
        tuple: A tuple of two base64-encoded strings for the price plot and boundary plot.
    """
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # --- Plot 1: Price Paths ---
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    num_steps = S.shape[0] - 1
    time_grid = np.linspace(0, num_steps, num_steps + 1)
    
    # Plot a subset of paths to keep the visualization clean
    paths_to_plot = S[:num_simulacoes]
    ax1.plot(time_grid, paths_to_plot, lw=1, alpha=0.7)
    ax1.set_title(f'Simulated Stock Price Paths')
    ax1.set_xlabel('Time Steps')
    ax1.set_ylabel('Stock Price')
    ax1.grid(True)
    
    buf1 = io.BytesIO()
    fig1.savefig(buf1, format='png', bbox_inches='tight')
    price_plot_base64 = base64.b64encode(buf1.getvalue()).decode('utf-8')
    buf1.close()
    plt.close(fig1)

    # --- Plot 2: Exercise Boundary ---
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.plot(time_grid, exercise_boundary, 'r-o', label='Optimal Exercise Boundary')
    title = f'American {option_type.capitalize()} Option Exercise Boundary'
    ax2.set_title(title)
    ax2.set_xlabel('Time Steps')
    ax2.set_ylabel('Stock Price')
    ax2.legend()
    ax2.grid(True)
    
    buf2 = io.BytesIO()
    fig2.savefig(buf2, format='png', bbox_inches='tight')
    boundary_plot_base64 = base64.b64encode(buf2.getvalue()).decode('utf-8')
    buf2.close()
    plt.close(fig2)

    return price_plot_base64, boundary_plot_base64

