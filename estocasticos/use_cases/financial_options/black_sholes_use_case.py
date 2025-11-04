import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from scipy.stats import norm

class BlackScholesModelUseCase:
    def __init__(self, S, E, r, sigma, T, option_type='call'):
        self.S = S  # Price of the underlying asset
        self.E = E  # Exercise price
        self.r = r / 100  # Interest rate (converted from percentage)
        self.sigma = sigma / 100  # Volatility (converted from percentage)
        self.T = T / 365  # Time to expiration in years (converted from days)
        self.option_type = option_type  # 'call' or 'put'

    def calculate_d_values(self):
        """Calculate d1, d2, and their CDFs N(d1), N(d2)."""
        d1 = (np.log(self.S / self.E) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        n_d1 = norm.cdf(d1)
        n_d2 = norm.cdf(d2)
        return d1, d2, n_d1, n_d2
        
    def calculate_price(self):
        d1, d2, n_d1, n_d2 = self.calculate_d_values()
        if self.option_type == 'call':
            price = self.S * n_d1 - self.E * np.exp(-self.r * self.T) * n_d2
        else:  # put option
            price = self.E * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1)
            
        return round(price, 2)
    
    def calculate_greeks(self):
        d1, d2, n_d1, n_d2 = self.calculate_d_values()
        
        # Delta (sensitivity to underlying price change)
        if self.option_type == 'call':
            delta = n_d1
        else:
            delta = n_d1 - 1
        
        # Gamma (sensitivity of delta to underlying price change)
        gamma = norm.pdf(d1) / (self.S * self.sigma * np.sqrt(self.T))
        
        # Theta (sensitivity to time decay)
        term1 = -self.S * norm.pdf(d1) * self.sigma / (2 * np.sqrt(self.T))
        if self.option_type == 'call':
            term2 = -self.r * self.E * np.exp(-self.r * self.T) * n_d2
            theta = term1 + term2
        else:
            term2 = self.r * self.E * np.exp(-self.r * self.T) * norm.cdf(-d2)
            theta = term1 + term2
        
        # Vega (sensitivity to volatility changes)
        vega = self.S * np.sqrt(self.T) * norm.pdf(d1) * 0.01  # 1% change in volatility
        
        return {
            'delta': round(delta, 4),
            'gamma': round(gamma, 4),
            'theta': round(theta / 365, 4),  # Daily theta
            'vega': round(vega, 4)
        }
    
    def plot_price_vs_underlying(self):
        # Create range of underlying prices (±30% from current)
        price_range = np.linspace(self.S * 0.7, self.S * 1.3, 100)
        option_prices = []
        
        for price in price_range:
            temp_model = BlackScholesModelUseCase(price, self.E, self.r * 100, self.sigma * 100, self.T * 365, self.option_type)
            option_prices.append(temp_model.calculate_price())
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(price_range, option_prices, 'b-', linewidth=2)
        ax.axvline(x=self.S, color='r', linestyle='--', alpha=0.7)
        ax.axhline(y=self.calculate_price(), color='g', linestyle='--', alpha=0.7)
        
        # Mark the current price point
        ax.plot(self.S, self.calculate_price(), 'ro', markersize=8)
        
        # Add break-even point
        if self.option_type == 'call':
            break_even = self.E + self.calculate_price()
            label = 'Break-even point'
        else:
            break_even = self.E - self.calculate_price()
            label = 'Break-even point'
        
        ax.axvline(x=break_even, color='purple', linestyle='-.', alpha=0.7)
        
        ax.set_title(f'Option Price vs Underlying Asset Price ({self.option_type.capitalize()} Option)')
        ax.set_xlabel('Underlying Asset Price')
        ax.set_ylabel('Option Price')
        ax.grid(True, alpha=0.3)
        
        # Add annotations
        ax.annotate(f'Current Price: {self.S}', xy=(self.S, 0), xytext=(self.S, max(option_prices)*0.1),
                   arrowprops=dict(arrowstyle="->", color='r'), ha='center')
        
        ax.annotate(f'Option Price: {self.calculate_price()}', xy=(self.S*0.75, self.calculate_price()), 
                   xytext=(self.S*0.75, self.calculate_price()), ha='right')
        
        ax.annotate(label, xy=(break_even, 0), xytext=(break_even, max(option_prices)*0.2),
                   arrowprops=dict(arrowstyle="->", color='purple'), ha='center')
        
        # Save plot to a base64 string
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        return base64.b64encode(image_png).decode('utf-8')
    
    def plot_payoff_at_expiration(self):
        # Create range of underlying prices (±50% from exercise price)
        price_range = np.linspace(self.E * 0.5, self.E * 1.5, 100)
        
        # Calculate payoffs at expiration
        if self.option_type == 'call':
            payoffs = np.maximum(price_range - self.E, 0) - self.calculate_price()
        else:
            payoffs = np.maximum(self.E - price_range, 0) - self.calculate_price()
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(price_range, payoffs, 'b-', linewidth=2)
        
        # Add break-even point
        if self.option_type == 'call':
            break_even = self.E + self.calculate_price()
        else:
            break_even = self.E - self.calculate_price()
        
        ax.axvline(x=break_even, color='purple', linestyle='-.', alpha=0.7)
        
        # Add current price
        ax.axvline(x=self.S, color='r', linestyle='--', alpha=0.7)
        
        # Add exercise price
        ax.axvline(x=self.E, color='g', linestyle='--', alpha=0.7)
        
        # Add zero line
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        
        ax.set_title(f'Payoff at Expiration ({self.option_type.capitalize()} Option)')
        ax.set_xlabel('Underlying Asset Price at Expiration')
        ax.set_ylabel('Profit/Loss')
        ax.grid(True, alpha=0.3)
        
        # Add annotations
        ax.annotate(f'Break-even: {round(break_even, 2)}', xy=(break_even, 0), 
                   xytext=(break_even, max(abs(min(payoffs)), max(payoffs))*0.2),
                   arrowprops=dict(arrowstyle="->", color='purple'), ha='center')
        
        ax.annotate(f'Current Price: {self.S}', xy=(self.S, 0), 
                   xytext=(self.S, max(abs(min(payoffs)), max(payoffs))*0.4),
                   arrowprops=dict(arrowstyle="->", color='r'), ha='center')
        
        ax.annotate(f'Exercise Price: {self.E}', xy=(self.E, 0), 
                   xytext=(self.E, max(abs(min(payoffs)), max(payoffs))*0.6),
                   arrowprops=dict(arrowstyle="->", color='g'), ha='center')
        
        if self.option_type == 'call':
            ax.annotate(f'Max Loss: -{self.calculate_price()}', xy=(self.E*0.5, -self.calculate_price()), 
                       xytext=(self.E*0.6, -self.calculate_price()), ha='left', va='bottom')
        else:
            ax.annotate(f'Max Loss: -{self.calculate_price()}', xy=(self.E*1.5, -self.calculate_price()), 
                       xytext=(self.E*1.4, -self.calculate_price()), ha='right', va='bottom')
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        return base64.b64encode(image_png).decode('utf-8')

    def generate_probability_curve(self, S0, sigma, T, r):
        # Time in years
        T_years = T / 365.0
        
        # Asset price range for the curve
        S_range = np.linspace(S0 * 0.5, S0 * 1.5, 300)
        
        # Parameters for lognormal distribution
        mu = (r - 0.5 * sigma**2) * T_years + np.log(S0)
        variance = sigma**2 * T_years
        pdf = (1 / (S_range * np.sqrt(2 * np.pi * variance))) * np.exp(- (np.log(S_range) - mu)**2 / (2 * variance))
        
        # Plot
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(S_range, pdf, color='blue')
        ax.set_title('Probability Density of Asset Price at Expiration')
        ax.set_xlabel('Asset Price at Expiration')
        ax.set_ylabel('Probability Density')
        ax.grid(True)
        # Save to base64
        buffer = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        image_base64 = base64.b64encode(image_png).decode('utf-8')
        return image_base64
