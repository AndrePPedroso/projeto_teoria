import numpy as np
import matplotlib.pyplot as plt
import io
import base64


class RandomWalkUseCase:
    def __init__(self, steps):
        self.steps = steps

    def random_walk(self, dist_type="normal"):
        X = np.zeros(self.steps)
        for t in range(1, self.steps):
            if dist_type == "normal":
                epsilon = np.random.normal(0, 1)  # Distribuição Normal
            elif dist_type == "uniform":
                epsilon = np.random.uniform(-1, 1)  # Distribuição Uniforme
            elif dist_type == "discrete":
                epsilon = np.random.choice([-1, 1])  # Distribuição Discreta {-1, 1}
            X[t] = X[t - 1] + epsilon
        return X

    # Função para gerar o gráfico com as três distribuições
    def generate_plot(self):
        rw_normal = self.random_walk(dist_type="normal")
        rw_uniform = self.random_walk(dist_type="uniform")
        rw_discrete = self.random_walk(dist_type="discrete")

        plt.figure(figsize=(10, 6))
        plt.plot(rw_normal, label="Normal distribution")
        plt.plot(rw_uniform, label="Uniform Distribution")
        plt.plot(rw_discrete, label="Discrete Distribution  {-1, 1}")
        plt.title("Random Walk with different distributions")
        plt.xlabel("Steps")
        plt.ylabel("X value")
        plt.legend()
        plt.grid(True)

        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        return base64.b64encode(image_png).decode("utf-8")
