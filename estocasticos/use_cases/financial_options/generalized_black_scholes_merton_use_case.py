import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import base64
from io import BytesIO

class GeneralizedBlackScholesMertonUseCase:
    def __init__(self, S, E, r, sigma, T, option_type, cost_of_carry, dividend_yield=0):
        """
        Initialize the Generalized Black-Scholes-Merton model with parameters.
        
        Parameters:
        S: Current price of the underlying asset
        E: Exercise (strike) price
        r: Risk-free interest rate (decimal)
        sigma: Volatility of the underlying asset (decimal)
        T: Time to expiration (in days)
        option_type: 'call' or 'put'
        cost_of_carry: Cost of carry 'b' (decimal)
        dividend_yield: Dividend yield 'q' (decimal)
        """
        self.S = S
        self.E = E
        self.r = r / 100  # Convert percentage to decimal
        self.sigma = sigma / 100  # Convert percentage to decimal
        self.T = T / 365  # Convert days to years
        self.option_type = option_type.lower()
        self.q = dividend_yield / 100  # Convert percentage to decimal
        self.b = self.r - self.q - cost_of_carry / 100  # Convert percentage to decimal
        
    def calculate_d_values(self):
        """Calculate d1, d2, and their CDFs N(d1), N(d2)."""
        d1 = (np.log(self.S / self.E) + (self.b + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        n_d1 = norm.cdf(d1)
        n_d2 = norm.cdf(d2)
        return d1, d2, n_d1, n_d2
    
    def calculate_price(self):
        """Calculate the option price using the Generalized BSM formula."""
        d1, d2, n_d1, n_d2 = self.calculate_d_values()
        
        if self.option_type == 'call':
            price = self.S * np.exp((self.b - self.r) * self.T) * n_d1 - self.E * np.exp(-self.r * self.T) * n_d2
        else:  # put option
            price = self.E * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * np.exp((self.b - self.r) * self.T) * norm.cdf(-d1)
        
        return round(price, 2)
    
    def calculate_greeks(self):
        """Calculate option Greeks: Delta, Gamma, Theta, Vega, and Rho."""
        d1, d2, n_d1, n_d2 = self.calculate_d_values()
        
        # Delta
        if self.option_type == 'call':
            delta = np.exp((self.b - self.r) * self.T) * n_d1
        else:
            delta = np.exp((self.b - self.r) * self.T) * (n_d1 - 1)
        
        # Gamma
        gamma = norm.pdf(d1) * np.exp((self.b - self.r) * self.T) / (self.S * self.sigma * np.sqrt(self.T))
        
        # Theta
        term1 = - (self.S * norm.pdf(d1) * self.sigma * np.exp((self.b - self.r) * self.T)) / (2 * np.sqrt(self.T))
        if self.option_type == 'call':
            term2 = - (self.b - self.r) * self.S * np.exp((self.b - self.r) * self.T) * n_d1
            term3 = - self.r * self.E * np.exp(-self.r * self.T) * n_d2
            theta = term1 + term2 + term3
        else: # put
            term2 = (self.b - self.r) * self.S * np.exp((self.b - self.r) * self.T) * norm.cdf(-d1)
            term3 = self.r * self.E * np.exp(-self.r * self.T) * norm.cdf(-d2)
            theta = term1 + term2 + term3

        theta /= 365 # Daily decay
        
        # Vega
        vega = self.S * np.exp((self.b - self.r) * self.T) * norm.pdf(d1) * np.sqrt(self.T) / 100 # per 1% change
        
        # Rho
        if self.option_type == 'call':
            rho = self.T * self.E * np.exp(-self.r * self.T) * n_d2 / 100 # per 1% change
        else:
            rho = -self.T * self.E * np.exp(-self.r * self.T) * norm.cdf(-d2) / 100
        
        return {
            'delta': round(delta, 4),
            'gamma': round(gamma, 4),
            'theta': round(theta, 4),
            'vega': round(vega, 4),
            'rho': round(rho, 4)
        }

    def _to_base64(self, fig):
        """Convert matplotlib figure to base64 string for embedding in HTML."""
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        return base64.b64encode(image_png).decode('utf-8')

    def plot_price_vs_underlying(self):
        """Generate a plot of option price vs underlying asset price."""
        price_range = np.linspace(self.S * 0.5, self.S * 1.5, 100)
        option_prices = []
        
        for price in price_range:
            temp_model = GeneralizedBlackScholesMertonUseCase(
                price, self.E, self.r * 100, self.sigma * 100, self.T * 365, 
                self.option_type, self.b * 100
            )
            option_prices.append(temp_model.calculate_price())
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(price_range, option_prices, 'b-', linewidth=2)
        ax.axvline(x=self.S, color='r', linestyle='--', alpha=0.5)
        ax.axhline(y=self.calculate_price(), color='r', linestyle='--', alpha=0.5)
        ax.set_xlabel('Underlying Asset Price')
        ax.set_ylabel('Option Price')
        ax.set_title(f'{"Call" if self.option_type == "call" else "Put"} Option Price vs Underlying Asset Price')
        ax.grid(True, alpha=0.3)
        
        return self._to_base64(fig)

    def plot_payoff_at_expiration(self):
        """Generate a plot of option payoff at expiration."""
        price_range = np.linspace(self.E * 0.5, self.E * 1.5, 100)
        option_price = self.calculate_price()
        
        if self.option_type == 'call':
            payoffs = [max(0, price - self.E) - option_price for price in price_range]
        else:
            payoffs = [max(0, self.E - price) - option_price for price in price_range]
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(price_range, payoffs, 'g-', linewidth=2)
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        ax.axvline(x=self.E, color='r', linestyle='--', alpha=0.5)
        
        if self.option_type == 'call':
            break_even = self.E + option_price
        else:
            break_even = self.E - option_price
        
        ax.axvline(x=break_even, color='b', linestyle='--', alpha=0.5)
        
        ax.set_xlabel('Underlying Asset Price at Expiration')
        ax.set_ylabel('Profit/Loss')
        ax.set_title(f'{"Call" if self.option_type == "call" else "Put"} Option Payoff at Expiration')
        ax.grid(True, alpha=0.3)
        
        return self._to_base64(fig)
