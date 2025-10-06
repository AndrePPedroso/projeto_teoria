import numpy as np
import matplotlib.pyplot as plt
import io
import base64

class ComparacaoModelosUseCase:
    def __init__(self, S0, mu_gbm, sigma_gbm, mu_mr, kappa_mr, sigma_mr, T, dt):
        self.S0 = S0
        self.mu_gbm = mu_gbm
        self.sigma_gbm = sigma_gbm
        self.mu_mr = mu_mr
        self.kappa_mr = kappa_mr
        self.sigma_mr = sigma_mr
        self.T = T
        self.dt = dt
        self.steps = int(T / dt)

    def _simulate_random_walk(self):
        X = np.zeros(self.steps)
        X[0] = self.S0
        for t in range(1, self.steps):
            epsilon = np.random.normal(0, 1)
            X[t] = X[t - 1] + epsilon
        return X

    def _simulate_gbm(self):
        n_steps = self.steps
        simulations = np.zeros(n_steps)
        simulations[0] = self.S0

        for i in range(1, n_steps):
            Z = np.random.normal(size=1)
            dW = Z * np.sqrt(self.dt)
            dS = self.mu_gbm * simulations[i - 1] * self.dt + self.sigma_gbm * simulations[i - 1] * dW
            simulations[i] = simulations[i - 1] + dS
        return simulations

    def _simulate_mean_reversion(self):
        n_steps = self.steps
        simulations = np.zeros(n_steps)
        simulations[0] = self.S0

        for t in range(1, n_steps):
            Z = np.random.normal(size=1)
            dW = Z * np.sqrt(self.dt)
            dS = self.kappa_mr * (self.mu_mr - simulations[t - 1]) * self.dt + self.sigma_mr * dW
            simulations[t] = simulations[t - 1] + dS
        return simulations

    def generate_plot(self):
        time_grid = np.linspace(0, self.T, self.steps)
        rw_path = self._simulate_random_walk()
        gbm_path = self._simulate_gbm()
        mr_path = self._simulate_mean_reversion()

        plt.figure(figsize=(12, 7))
        plt.plot(time_grid, rw_path, label="Random Walk")
        plt.plot(time_grid, gbm_path, label="Geometric Brownian Motion")
        plt.plot(time_grid, mr_path, label="Mean Reversion")
        
        plt.title("Comparação de Modelos Estocásticos")
        plt.xlabel("Tempo")
        plt.ylabel("Valor")
        plt.legend()
        plt.grid(True)

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        return base64.b64encode(image_png).decode('utf-8')
