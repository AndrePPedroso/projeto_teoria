import numpy as np
import io
import base64
import matplotlib.pyplot as plt


class CadeiaMarkovUseCase:
    def __init__(
        self, num_states, states, transition_matrix, initial_percentages, steps
    ):
        self.num_states = num_states
        self.states = states
        self.transition_matrix = np.array(transition_matrix)
        self.initial_state = np.array(initial_percentages) / sum(
            initial_percentages
        )  # Normalize
        self.steps = steps

    def simulate(self):
        evolution = [self.initial_state]
        current_state = self.initial_state

        for _ in range(self.steps):
            current_state = np.dot(current_state, self.transition_matrix)
            evolution.append(current_state)

        return np.array(evolution)

    def generate_plot(self, evolution):
        plt.figure(figsize=(8, 6))
        steps = len(evolution) - 1

        for i, state in enumerate(self.states):
            plt.plot(
                range(steps + 1),
                evolution[:, i] * 100,
                marker="o",
                label=f"State {state}",
            )

        plt.title("Evolution of State Probabilities Over Time")
        plt.xlabel("Iterations")
        plt.ylabel("Percentage (%)")
        plt.grid(True)
        plt.legend()

        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        return base64.b64encode(image_png).decode("utf-8")
