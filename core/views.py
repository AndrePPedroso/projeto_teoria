from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from estocasticos.use_cases.random_walk_normal_use_case import RandomWalkNormalUseCase
from estocasticos.use_cases.cadeia_markov_use_case import CadeiaMarkovUseCase
from estocasticos.use_cases.random_walk_use_case import RandomWalkUseCase


def custom_admin_login(request):
    error_message = None 
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('/home')
        else:
            error_message = "Usuário ou senha incorretos." 

    else:
        form = AuthenticationForm()
    
    return render(request, "admin/login.html", {"form": form, "error_message": error_message})

def home_view(request):
    return render(request, 'site/home/home.html') 

def processos_home(request):
    return render(request, 'site/processos-estocasticos/processos_home.html')

#--------------------------- navegação---------------------------------

def cadeia_markov(request):
    return render(request, 'site/processos-estocasticos/cadeia_markov.html')

def random_walk_normal(request):
    return render(request, 'site/processos-estocasticos/random_walk_normal.html')

def random_walk(request):
    return render(request, 'site/processos-estocasticos/random_walk.html')

def teoria_opcoes_financeiras(request):
    return render(request, 'partials/teoria_opcoes_financeiras.html')

def teoria_opcoes_reais(request):
    return render(request, 'partials/teoria_opcoes_reais.html')

#--------------------------- calculo---------------------------------

@csrf_exempt
def markov_simulator(request):
    if request.method == 'POST':
        try:
            # Extraia os dados do formulário
            num_states = int(request.POST['num_states'])
            states = request.POST['states'].split(',')
            transition_matrix = [
                [float(request.POST[f"transition_matrix[{i}][{j}]"]) for j in range(num_states)]
                for i in range(num_states)
            ]
            initial_percentages = [
                float(request.POST[f'initial_percentages[{i}]']) for i in range(num_states)
            ]
            steps = int(request.POST['iterations'])

            # Instancie o Use Case e realize a simulação
            simulator = CadeiaMarkovUseCase(num_states, states, transition_matrix, initial_percentages, steps)
            evolution = simulator.simulate()
            plot = simulator.generate_plot(evolution)

            # Retorne o gráfico como JSON
            return JsonResponse({'plot': plot})

        except Exception as e:
            # Retorne o erro para depuração
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'markov.html')

def random_walk_normal_view(request):
    if request.method == 'POST':
        steps = int(request.POST['steps'])
        paths = int(request.POST['paths'])
        
        simulator = RandomWalkNormalUseCase(steps, paths)
        
        # Gerar o gráfico dos caminhos do Random Walk
        walk_plot = simulator.plot_walks()
        
        # Gerar os histogramas e obter as estatísticas
        histograms_plot, statistics = simulator.plot_histograms_and_statistics()
        
        return JsonResponse({
            'walk_plot': walk_plot,
            'histograms_plot': histograms_plot,
            'statistics': statistics
        })
    
    return render(request, 'random_walk.html')


def random_walk_view(request):
    if request.method == 'POST':
        steps = int(request.POST.get('steps', 1000))  # Valor padrão de 1000 passos
        visualizer = RandomWalkUseCase(steps)
        
        # Gera o gráfico e obtém a imagem em base64
        plot_image = visualizer.generate_plot()
        
        return JsonResponse({'plot_image': plot_image})
    
    return render(request, 'random_walk_visualization.html')
