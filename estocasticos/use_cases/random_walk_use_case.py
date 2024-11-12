import numpy as np
import matplotlib.pyplot as plt
import io
import base64

class RandomWalkUseCase:
    def __init__(self, steps):
        self.steps = steps

    def random_walk(self, dist_type='normal'):
        X = np.zeros(self.steps)
        for t in range(1, self.steps):
            if dist_type == 'normal':
                epsilon = np.random.normal(0, 1)  # Distribuição Normal
            elif dist_type == 'uniform':
                epsilon = np.random.uniform(-1, 1)  # Distribuição Uniforme
            elif dist_type == 'discrete':
                epsilon = np.random.choice([-1, 1])  # Distribuição Discreta {-1, 1}
            X[t] = X[t-1] + epsilon
        return X

    # Função para gerar o gráfico com as três distribuições
    def generate_plot(self):
        rw_normal = self.random_walk(dist_type='normal')
        rw_uniform = self.random_walk(dist_type='uniform')
        rw_discrete = self.random_walk(dist_type='discrete')

        plt.figure(figsize=(10, 6))
        plt.plot(rw_normal, label='Distribuição Normal')
        plt.plot(rw_uniform, label='Distribuição Uniforme')
        plt.plot(rw_discrete, label='Distribuição Discreta {-1, 1}')
        plt.title('Random Walk com diferentes distribuições')
        plt.xlabel('Passos')
        plt.ylabel('Valor de X')
        plt.legend()
        plt.grid(True)

        # Salvar o gráfico em um formato base64 para exibir em uma página web
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        return base64.b64encode(image_png).decode('utf-8')
