import numpy as np
import matplotlib.pyplot as plt
import io
import base64


class GeneralizedBrownianMotionUseCase:
    def __init__(self, S0, mu, sigma, T, dt, n_simulations):
        self.S0 = S0
        self.mu = mu
        self.sigma = sigma
        self.T = T
        self.dt = dt
        self.n_simulations = n_simulations

    def simulate_paths(self):
        n_steps = int(self.T / self.dt)
        time_grid = np.linspace(0, self.T, n_steps)

        simulations = np.zeros((self.n_simulations, n_steps))
        simulations[:, 0] = self.S0

        for i in range(1, n_steps):
            Z = np.random.normal(size=self.n_simulations)
            dW = Z * np.sqrt(self.dt)
            dS = (
                self.mu * simulations[:, i - 1] * self.dt
                + self.sigma * simulations[:, i - 1] * dW
            )
            simulations[:, i] = simulations[:, i - 1] + dS

        return time_grid, simulations

    def plot_paths(self, time_grid, simulations):
        fig, ax = plt.subplots(figsize=(10, 6))
        for sim in simulations:
            ax.plot(time_grid, sim, lw=0.8, alpha=0.6)
        ax.set_title("Caminhos Simulados - Processo Browniano Generalizado")
        ax.set_xlabel("Tempo")
        ax.set_ylabel("Preço")

        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        return base64.b64encode(image_png).decode("utf-8")

    def plot_distribution(self, simulations):
        final_prices = simulations[:, -1]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(final_prices, bins=30, alpha=0.7, color="green", edgecolor="black")
        ax.set_title("Distribuição dos Preços Finais")
        ax.set_xlabel("Preço Final")
        ax.set_ylabel("Frequência")

        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        return base64.b64encode(image_png).decode("utf-8")

    def calculate_statistics(self, simulations):
        final_prices = simulations[:, -1]
        stats = {
            "Média": np.mean(final_prices),
            "Desvio Padrão": np.std(final_prices),
            "Variância": np.var(final_prices),
            "Mínimo": np.min(final_prices),
            "Máximo": np.max(final_prices),
        }
        return stats
