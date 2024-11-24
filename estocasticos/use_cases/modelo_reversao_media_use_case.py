import numpy as np
import matplotlib.pyplot as plt
import io
import base64

class ReversaoMediaUseCase:
    def __init__(self, S0, mu, kappa, sigma, T, dt, n_simulations):
        self.S0 = S0
        self.mu = mu
        self.kappa = kappa
        self.sigma = sigma
        self.T = T
        self.dt = dt
        self.n_simulations = n_simulations

    def simulate(self):
        n_steps = int(self.T / self.dt)
        time_grid = np.linspace(0, self.T, n_steps)

        simulations = np.zeros((self.n_simulations, n_steps))
        simulations[:, 0] = self.S0

        for t in range(1, n_steps):
            Z = np.random.normal(size=self.n_simulations)
            dW = Z * np.sqrt(self.dt)
            dS = self.kappa * (self.mu - simulations[:, t-1]) * self.dt + self.sigma * dW
            simulations[:, t] = simulations[:, t-1] + dS

        return time_grid, simulations

    def plot_paths(self, time_grid, simulations):
        fig, ax = plt.subplots(figsize=(10, 6))
        for sim in simulations:
            ax.plot(time_grid, sim, lw=0.8, alpha=0.6)
        ax.set_title("Caminhos Simulados - Reversão à Média")
        ax.set_xlabel("Tempo")
        ax.set_ylabel("Valor")

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        return base64.b64encode(image_png).decode('utf-8')

    def plot_distribution(self, simulations):
        final_values = simulations[:, -1]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(final_values, bins=30, alpha=0.7, color='green', edgecolor='black')
        ax.set_title("Distribuição dos Valores Finais")
        ax.set_xlabel("Valor Final")
        ax.set_ylabel("Frequência")

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        return base64.b64encode(image_png).decode('utf-8')

    def calculate_statistics(self, simulations):
        final_values = simulations[:, -1]
        stats = {
            "Média": np.mean(final_values),
            "Desvio Padrão": np.std(final_values),
            "Variância": np.var(final_values),
            "Mínimo": np.min(final_values),
            "Máximo": np.max(final_values),
        }
        return stats