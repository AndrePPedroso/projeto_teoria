import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64


class MonteCarloUseCase:
    def __init__(self, S0, mu, sigma, time_unit, num_periods, num_simulations):
        self.S0 = S0
        self.mu = mu
        self.sigma = sigma
        self.time_unit = time_unit
        self.num_periods = num_periods
        self.num_simulations = num_simulations
        self.prices = None

    def run_simulation(self):
        dt = {"Dia": 1 / 252, "Semana": 1 / 52, "Mês": 1 / 12, "Ano": 1}.get(
            self.time_unit, 1
        )

        self.prices = np.zeros((self.num_simulations, self.num_periods + 1))
        self.prices[:, 0] = self.S0

        for i in range(self.num_simulations):
            for t in range(1, self.num_periods + 1):
                epsilon = np.random.normal(0, 1)
                delta_S = (self.mu * dt * self.prices[i, t - 1]) + (
                    self.sigma * np.sqrt(dt) * self.prices[i, t - 1] * epsilon
                )
                self.prices[i, t] = self.prices[i, t - 1] + delta_S

        return self.prices

    def plot_simulation(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        for i in range(self.num_simulations):
            ax.plot(self.prices[i], lw=0.8, alpha=0.6)
        ax.set_title("Price Evolution - Monte Carlo Simulation")
        ax.set_xlabel(f"{self.time_unit}(s)")
        ax.set_ylabel("Share price")

        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        return base64.b64encode(image_png).decode("utf-8")

    def get_final_price_distribution(self):
        final_prices = self.prices[:, -1]
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.hist(final_prices, bins=30, alpha=0.7, color="green", edgecolor="black")
        ax.set_title("Distribution of Final Prices")
        ax.set_xlabel("Share price")
        ax.set_ylabel("Frequency")

        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        return base64.b64encode(image_png).decode("utf-8")

    def get_statistics(self):
        final_prices = self.prices[:, -1]
        stats = {
            "Mean": np.mean(final_prices),
            "Desvio Padrão": np.std(final_prices),
            "Standard Deviation": np.var(final_prices),
            "Minimum": np.min(final_prices),
            "Maximum": np.max(final_prices),
        }
        return stats
