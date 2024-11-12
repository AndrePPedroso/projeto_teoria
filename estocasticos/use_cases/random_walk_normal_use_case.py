import numpy as np
import matplotlib.pyplot as plt
import io
import base64

class RandomWalkNormalUseCase:
    def __init__(self, steps, paths):
        self.steps = steps
        self.paths = paths
        self.walks = self._generate_walks()

    # Função privada para realizar o Random Walk
    def _generate_walks(self):
        walks = np.zeros((self.paths, self.steps))
        for i in range(self.paths):
            for t in range(1, self.steps):
                epsilon = np.random.normal(0, 1)
                walks[i, t] = walks[i, t-1] + epsilon
        return walks

    # Função para calcular as estatísticas descritivas
    def calculate_statistics(self, data):
        minimum = np.min(data)
        maximum = np.max(data)
        mean = np.mean(data)
        median = np.median(data)
        variance = np.var(data, ddof=1)
        std_dev = np.std(data, ddof=1)
        
        return {
            "Mínimo": minimum,
            "Máximo": maximum,
            "Média": mean,
            "Mediana": median,
            "Variância": variance,
            "Desvio-Padrão": std_dev
        }

    def plot_walks(self):
        plt.figure(figsize=(10, 6))
        for i in range(self.paths):
            plt.plot(self.walks[i], label=f'Caminho {i+1}')
        
        plt.title(f'Random Walk com {self.paths} caminhos e {self.steps} passos')
        plt.xlabel('Passos')
        plt.ylabel('Valor de X')
        plt.grid(True)
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        return base64.b64encode(image_png).decode('utf-8')

    def plot_histograms_and_statistics(self):
        steps_25 = self.steps // 4
        steps_50 = self.steps // 2
        steps_75 = (3 * self.steps) // 4

        divisions = [
            (self.walks[:, :steps_25], '0% - 25% dos Passos'),
            (self.walks[:, :steps_50], '0% - 50% dos Passos'),
            (self.walks[:, :steps_75], '0% - 75% dos Passos'),
            (self.walks[:, :], '0% - 100% dos Passos')
        ]

        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        stats_list = []

        for i, (data, label) in enumerate(divisions):
            flattened_data = data.flatten()
            stats = self.calculate_statistics(flattened_data)
            stats_list.append((label, stats))

            ax = axs[i // 2, i % 2]
            ax.hist(flattened_data, bins=30, edgecolor='black')
            ax.set_title(f'Distribuição {label}')
            ax.set_xlabel('Valor de X')
            ax.set_ylabel('Frequência')

        plt.tight_layout()
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        histograms_image = base64.b64encode(image_png).decode('utf-8')
        
        return histograms_image, stats_list
