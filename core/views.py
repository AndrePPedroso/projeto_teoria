from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def custom_admin_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # Redirect based on user type
            if user.is_superuser:
                return redirect('/admin/')  # Admin panel for superuser
            else:
                return redirect('/home')  # Home page for regular users
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, "admin/login.html", {"form": form})

def home_view(request):
    return render(request, 'site/home/home.html') 


def custom_404(request, exception):
    return redirect('/admin/login/')

def custom_403(request, exception=None):
    return redirect('/admin/login/')


def processos_home(request):
    return render(request, 'site/processos-estocasticos/processos_home.html')

def teoria_opcoes_financeiras(request):
    return render(request, 'partials/teoria_opcoes_financeiras.html')

def teoria_opcoes_reais(request):
    return render(request, 'partials/teoria_opcoes_reais.html')


# Function to simulate Markov chain evolution
def simulate_markov_chain(transition_matrix, initial_state, steps):
    evolution = [initial_state]
    current_state = initial_state

    for _ in range(steps):
        current_state = np.dot(current_state, transition_matrix)
        evolution.append(current_state)

    return np.array(evolution)

# Function to generate plot as base64 image
def generate_plot(states, evolution):
    plt.figure(figsize=(8, 6))
    steps = len(evolution) - 1

    for i, state in enumerate(states):
        plt.plot(range(steps + 1), evolution[:, i] * 100, marker='o', label=f'State {state}')

    plt.title('Evolution of State Probabilities Over Time')
    plt.xlabel('Iterations')
    plt.ylabel('Percentage (%)')
    plt.grid(True)
    plt.legend()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')

# Parse transition matrix from request.POST
def parse_transition_matrix(num_states, post_data):
    matrix = []
    for i in range(num_states):
        row = []
        for j in range(num_states):
            field_name = f"transition_matrix[{i}][{j}]"
            row.append(float(post_data[field_name]))  # Convert each entry to float
        matrix.append(row)
    return np.array(matrix)

@csrf_exempt
def markov_simulator(request):
    if request.method == 'POST':
        try:
            # Extract form data
            num_states = int(request.POST['num_states'])
            states = request.POST['states'].split(',')
            transition_matrix = parse_transition_matrix(num_states, request.POST)

            # Extract initial percentages
            initial_percentages = np.array([
                float(request.POST[f'initial_percentages[{i}]']) for i in range(num_states)
            ])
            initial_state = initial_percentages / sum(initial_percentages)  # Normalize percentages
            steps = int(request.POST['iterations'])

            # Simulate evolution
            evolution = simulate_markov_chain(transition_matrix, initial_state, steps)

            # Generate plot as base64 string
            plot = generate_plot(states, evolution)

            # Send the plot back as JSON data
            return JsonResponse({'plot': plot})

        except Exception as e:
            # Return error as JSON for debugging
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'markov.html')