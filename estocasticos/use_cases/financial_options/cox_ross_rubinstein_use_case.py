import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import math
import json

class CoxRossRubinsteinUseCase:
    def __init__(self, S, E, r, sigma, T, option_type, steps, dividend_yield=0):
        """
        Initialize the Cox-Ross-Rubinstein (Binomial) model with parameters.
        
        Parameters:
        S: Current price of the underlying asset
        E: Exercise (strike) price
        r: Risk-free interest rate (decimal)
        sigma: Volatility of the underlying asset (decimal)
        T: Time to expiration (in days)
        option_type: 'call' or 'put'
        steps: Number of time steps in the binomial tree
        dividend_yield: Continuous dividend yield (decimal)
        """
        self.S = S
        self.E = E
        self.r = r / 100  # Convert percentage to decimal
        self.sigma = sigma / 100  # Convert percentage to decimal
        self.T = T / 365  # Convert days to years
        self.option_type = option_type.lower()
        self.q = dividend_yield / 100  # Convert percentage to decimal
        self.steps = min(steps, 10)  # Limit to 10 steps max for visualization
        
    def calculate_price(self):
        """Calculate the option price using the binomial model."""
        tree_data = self.calculate_tree_data()
        return round(tree_data['option_tree'][0, 0], 2)
    
    def calculate_greeks(self):
        """Calculate option Greeks using finite difference approximations."""
        price = self.calculate_price()
        
        # Delta calculation (∂V/∂S)
        dS = self.S * 0.01
        delta_model = CoxRossRubinsteinUseCase(
            self.S + dS, self.E, self.r * 100, self.sigma * 100, 
            self.T * 365, self.option_type, self.steps, self.q * 100
        )
        delta = (delta_model.calculate_price() - price) / dS
        
        # Gamma calculation (∂²V/∂S²)
        delta_model_minus = CoxRossRubinsteinUseCase(
            self.S - dS, self.E, self.r * 100, self.sigma * 100, 
            self.T * 365, self.option_type, self.steps, self.q * 100
        )
        price_minus = delta_model_minus.calculate_price()
        gamma = (delta_model.calculate_price() - 2 * price + price_minus) / (dS ** 2)
        
        # Theta calculation (∂V/∂t)
        dt = 1  # 1 day
        if self.T * 365 > dt:  # Ensure we don't go negative with time
            theta_model = CoxRossRubinsteinUseCase(
                self.S, self.E, self.r * 100, self.sigma * 100, 
                self.T * 365 - dt, self.option_type, self.steps, self.q * 100
            )
            theta = (theta_model.calculate_price() - price) / dt
        else:
            theta = 0
        
        # Vega calculation (∂V/∂σ)
        dSigma = 0.01  # 1% change in volatility
        vega_model = CoxRossRubinsteinUseCase(
            self.S, self.E, self.r * 100, (self.sigma + dSigma) * 100, 
            self.T * 365, self.option_type, self.steps, self.q * 100
        )
        vega = (vega_model.calculate_price() - price) / (dSigma * 100)  # Vega per 1% change
        
        # Rho calculation (∂V/∂r)
        dR = 0.01  # 1% change in interest rate
        rho_model = CoxRossRubinsteinUseCase(
            self.S, self.E, (self.r + dR) * 100, self.sigma * 100, 
            self.T * 365, self.option_type, self.steps, self.q * 100
        )
        rho = (rho_model.calculate_price() - price) / (dR * 100)  # Rho per 1% change
        
        return {
            'delta': round(delta, 4),
            'gamma': round(gamma, 4),
            'theta': round(theta, 4),
            'vega': round(vega, 4),
            'rho': round(rho, 4)
        }
    
    def calculate_tree_data(self):
        """Calculate data for the binomial tree."""
        # Time step
        dt = self.T / self.steps
        
        # Calculate up and down factors
        u = np.exp(self.sigma * np.sqrt(dt))
        d = 1 / u
        
        # Risk-neutral probability
        a = np.exp((self.r - self.q) * dt)  # growth factor
        p = (a - d) / (u - d)
        
        # Create arrays to store the stock price tree and option value tree
        stock_tree = np.zeros((self.steps + 1, self.steps + 1))
        option_tree = np.zeros((self.steps + 1, self.steps + 1))
        
        # Build the stock price tree
        for i in range(self.steps + 1):
            for j in range(i + 1):
                stock_tree[j, i] = self.S * (u ** (i - j)) * (d ** j)
        
        # Calculate option values at expiration (last column)
        for j in range(self.steps + 1):
            if self.option_type == 'call':
                option_tree[j, self.steps] = max(0, stock_tree[j, self.steps] - self.E)
            else:  # put option
                option_tree[j, self.steps] = max(0, self.E - stock_tree[j, self.steps])
        
        # Work backwards through the tree
        for i in range(self.steps - 1, -1, -1):
            for j in range(i + 1):
                # European option valuation formula (risk-neutral pricing)
                option_tree[j, i] = np.exp(-self.r * dt) * (p * option_tree[j, i+1] + (1-p) * option_tree[j+1, i+1])
        
        return {
            'stock_tree': stock_tree,
            'option_tree': option_tree,
            'u': u,
            'd': d,
            'p': p,
            'dt': dt
        }
    
    def get_lattice_data(self):
        """Get data for table-based visualization of the lattice."""
        tree_data = self.calculate_tree_data()
        stock_tree = tree_data['stock_tree']
        option_tree = tree_data['option_tree']
        
        # Format data for table representation
        steps = self.steps
        
        # Structure data for visualization
        lattice_data = []
        
        # For each node in the tree (working top to bottom)
        for j in range(steps + 1):
            stock_row = []
            option_row = []
            intrinsic_row = []
            
            # For each time step
            for i in range(steps + 1):
                if j <= i:  # Valid nodes in the tree
                    stock_price = stock_tree[j, i]
                    option_value = option_tree[j, i]
                    
                    # Calculate intrinsic value
                    if self.option_type == 'call':
                        intrinsic_value = max(0, stock_price - self.E)
                    else:
                        intrinsic_value = max(0, self.E - stock_price)
                    
                    # Check if in-the-money
                    if self.option_type == 'call':
                        is_in_the_money = stock_price > self.E
                    else:
                        is_in_the_money = stock_price < self.E
                    
                    stock_row.append({
                        'value': round(stock_price, 2),
                        'in_the_money': is_in_the_money
                    })
                    option_row.append(round(option_value, 2))
                    intrinsic_row.append(round(intrinsic_value, 2))
                else:
                    stock_row.append(None)
                    option_row.append(None)
                    intrinsic_row.append(None)
            
            lattice_data.append({
                'node': j,
                'stock_prices': stock_row,
                'option_values': option_row,
                'intrinsic_values': intrinsic_row
            })
        
        return {
            'lattice': lattice_data,
            'u': round(tree_data['u'], 4),
            'd': round(tree_data['d'], 4),
            'p': round(tree_data['p'], 4),
            'dt': round(tree_data['dt'], 4),
            'steps': steps,
            'option_type': self.option_type,
            'strike_price': self.E
        }
    
    def generate_lattice_html(self):
        """Generate HTML for the binomial lattice visualization."""
        lattice_data = self.get_lattice_data()
        steps = lattice_data['steps']
        
        # Generate HTML
        html = '<div class="binomial-lattice">'
        html += '<table class="table table-bordered table-sm">'
        
        # Header row with time steps
        html += '<thead><tr><th>Time Step</th>'
        for t in range(steps + 1):
            html += f'<th>t={t}</th>'
        html += '</tr></thead><tbody>'
        
        # For each node, create rows for stock price, option value, and intrinsic value
        for node_data in lattice_data['lattice']:
            node = node_data['node']
            
            # Stock price row
            html += f'<tr><td>Stock Price (Node {node})</td>'
            for i, price in enumerate(node_data['stock_prices']):
                if price is not None:
                    css_class = 'bg-success bg-opacity-25' if price['in_the_money'] else ''
                    html += f'<td class="{css_class}">${price["value"]}</td>'
                else:
                    html += '<td>-</td>'
            html += '</tr>'
            
            # Option value row
            html += '<tr class="table-light"><td>Option Value (Node ' + str(node) + ')</td>'
            for i, value in enumerate(node_data['option_values']):
                if value is not None:
                    html += f'<td>${value}</td>'
                else:
                    html += '<td>-</td>'
            html += '</tr>'
            
            # Intrinsic value row
            html += '<tr class="table-secondary"><td>Intrinsic Value (Node ' + str(node) + ')</td>'
            for i, value in enumerate(node_data['intrinsic_values']):
                if value is not None:
                    html += f'<td>${value}</td>'
                else:
                    html += '<td>-</td>'
            html += '</tr>'
            
            # Add a separator row except for the last node
            if node < steps:
                html += '<tr><td colspan="' + str(steps + 2) + '" class="p-0"><hr class="m-0"></td></tr>'
        
        html += '</tbody></table>'
        
        # Add legend
        html += '<div class="alert alert-info mt-3">'
        html += '<p><strong>Legend:</strong><br>'
        html += 'Stock Price: Current value of the underlying asset at each node<br>'
        html += 'Option Value: Value of the option at each node<br>'
        html += 'Intrinsic Value: Immediate exercise value (max(0, S-K) for calls, max(0, K-S) for puts))<br>'
        html += '<span class="badge bg-success bg-opacity-25">Green cells</span> indicate where the option is in-the-money</p>'
        html += '</div>'
        
        html += '</div>'
        
        return html