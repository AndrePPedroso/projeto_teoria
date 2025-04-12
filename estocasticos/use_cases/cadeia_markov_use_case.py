# Updated Python backend code
import numpy as np
import io
import base64
import matplotlib.pyplot as plt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

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
        evolution = [self.initial_state.tolist()]  # Convert to list immediately
        current_state = self.initial_state
        
        for _ in range(self.steps):
            current_state = np.dot(current_state, self.transition_matrix)
            evolution.append(current_state.tolist())  # Convert each state to list
        
        return evolution  # Already a list of lists
    
    def generate_plot(self, evolution):
        plt.figure(figsize=(8, 6))
        steps = len(evolution) - 1
        
        for i, state in enumerate(self.states):
            plt.plot(
                range(steps + 1),
                [state_vector[i] * 100 for state_vector in evolution], 
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

@csrf_exempt
def markov_simulator(request):
    if request.method == "POST":
        try:
            num_states = int(request.POST["num_states"])
            states = request.POST["states"].split(",")
            transition_matrix = [
                [
                    float(request.POST[f"transition_matrix[{i}][{j}]"])
                    for j in range(num_states)
                ]
                for i in range(num_states)
            ]
            initial_percentages = [
                float(request.POST[f"initial_percentages[{i}]"])
                for i in range(num_states)
            ]
            steps = int(request.POST["iterations"])
            simulator = CadeiaMarkovUseCase(
                num_states, states, transition_matrix, initial_percentages, steps
            )
            evolution = simulator.simulate()
            plot = simulator.generate_plot(evolution)

            # Debug the evolution data before sending
            print("Debug - Evolution type:", type(evolution))
            print("Debug - Evolution data:", evolution[:2] if len(evolution) > 2 else evolution)
            print("Debug - States:", states)
            
            # Return both the plot and the evolution matrix
            # No need to call tolist() as we're already storing as lists during simulation
            return JsonResponse({
                "plot": plot, 
                "evolution": evolution,  # Already a list of lists
                "states": states,
                "iterations": steps
            }, json_dumps_params={'indent': 2})  # Pretty printing for debugging

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, "markov.html")