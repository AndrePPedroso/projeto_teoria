from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from estocasticos.use_cases.mbg_ito_use_case import GeneralizedBrownianMotionUseCase
from estocasticos.use_cases.modelo_reversao_media_use_case import ReversaoMediaUseCase
from estocasticos.use_cases.monte_carlos_use_case import MonteCarloUseCase
from estocasticos.use_cases.random_walk_normal_use_case import RandomWalkNormalUseCase
from estocasticos.use_cases.cadeia_markov_use_case import CadeiaMarkovUseCase
from estocasticos.use_cases.random_walk_use_case import RandomWalkUseCase


@login_required(login_url='/admin/login/')
def processos_home(request):
    return render(request, "site/processos-estocasticos/processos_home.html")


def cadeia_markov(request):
    return render(request, "site/processos-estocasticos/cadeia_markov.html")


def random_walk_normal(request):
    return render(request, "site/processos-estocasticos/random_walk_normal.html")


def random_walk_template(request):
    try:
        context = {}
        return render(request, "site/processos-estocasticos/random_walk.html", context)
    except Exception as e:
        import logging

        logging.error(f"Error rendering random_walk_template: {e}")
        return render(request, "error_page.html", {"error": str(e)})


def monte_carlos(request):
    return render(request, "site/processos-estocasticos/monte_carlos.html")


def mbg_ito(request):
    return render(request, "site/processos-estocasticos/mbg_ito.html")


@login_required(login_url='/admin/login/')
def mbg_teoria(request):
    return render(request, "site/teoria/mbg.html")


def modelo_reversao_media(request):
    return render(request, "site/processos-estocasticos/modelo_media.html")


@login_required(login_url='/admin/login/')
def teoria_opcoes_financeiras(request):
    return render(request, "partials/teoria_opcoes_financeiras.html")


@login_required(login_url='/admin/login/')
def teoria_opcoes_reais(request):
    return render(request, "partials/teoria_opcoes_reais.html")


# --------------------------- calculos-----------------------------


@csrf_exempt
def markov_simulator(request):
    """
    View function to handle the Markov chain simulation.
    Accepts POST requests with form data containing Markov chain parameters.
    Returns JSON with plot image and evolution matrix.
    """
    if request.method == "POST":
        try:
            # Parse input parameters from the form
            num_states = int(request.POST["num_states"])
            states = [s.strip() for s in request.POST["states"].split(",")]
            
            # Parse transition matrix
            transition_matrix = []
            try:
                for i in range(num_states):
                    row = []
                    for j in range(num_states):
                        prob = float(request.POST[f"transition_matrix[{i}][{j}]"])
                        row.append(prob)
                    transition_matrix.append(row)
            except ValueError:
                return JsonResponse({"error": "Invalid transition matrix values."}, status=400)
            
            # Parse initial percentages
            initial_percentages = []
            for i in range(num_states):
                percentage = float(request.POST[f"initial_percentages[{i}]"])
                initial_percentages.append(percentage)
            
            # Get number of iterations
            steps = int(request.POST["iterations"])
            
            # Create and run the simulation
            simulator = CadeiaMarkovUseCase(
                num_states, states, transition_matrix, initial_percentages, steps
            )
            
            # Get evolution matrix and generate plot
            evolution = simulator.simulate()
            plot = simulator.generate_plot(evolution)
            
            # Return JSON response with both the plot and evolution matrix
            return JsonResponse({
                "plot": plot, 
                "evolution": evolution,
                "states": states,
                "iterations": steps
            })

        except Exception as e:
            # Return error if anything goes wrong
            return JsonResponse({"error": str(e)}, status=500)

    # For GET requests, render the form template
    return render(request, "markov.html")


def random_walk_normal_view(request):
    if request.method == "POST":
        current_language = request.session["language"]

        steps = request.POST["steps"]
        paths = request.POST["paths"]

        if not steps or not paths:
            if current_language == 'pt':
                return JsonResponse({"error": "Parâmetros de entrada inválidos."}, status=200)
            else: 
                return JsonResponse({"error": "Invalid input parameters."}, status=200)
            
        steps = int(steps)
        paths = int(paths)

        if steps > 100 or paths > 20:
            if current_language == 'pt':
                return JsonResponse(
                    {"error": "O número de passos deve ser <= 100 e o número de caminhos <= 20."}, status=200
                )
            else:
                return JsonResponse(
                    {"error": "Number of steps must be <= 100 and paths <= 20."}, status=200
                )

        simulator = RandomWalkNormalUseCase(steps, paths)

        walk_plot = simulator.plot_walks()
        histograms_plot, statistics = simulator.plot_histograms_and_statistics()

        return JsonResponse(
            {
                "walk_plot": walk_plot,
                "histograms_plot": histograms_plot,
                "statistics": statistics,
                "language": current_language,
            }
        )


def random_walk_view(request):
    if request.method == "POST":
        steps = int(request.POST.get("steps", 1000))  # Valor padrão de 1000 passos
        visualizer = RandomWalkUseCase(steps)

        # Gera o gráfico e obtém a imagem em base64
        plot_image = visualizer.generate_plot()

        return JsonResponse({"plot_image": plot_image})

    return render(request, "random_walk_visualization.html")


def monte_carlo_view(request):
    if request.method == "POST":
        S0 = float(request.POST.get("S0", 100))
        mu = float(request.POST.get("mu", 0.15))
        sigma = float(request.POST.get("sigma", 0.3))
        time_unit = request.POST.get("time_unit", "Ano")
        num_periods = int(request.POST.get("num_periods", 10))
        num_simulations = int(request.POST.get("num_simulations", 100))

        simulator = MonteCarloUseCase(
            S0, mu, sigma, time_unit, num_periods, num_simulations
        )
        prices = simulator.run_simulation()
        price_plot = simulator.plot_simulation()
        distribution_plot = simulator.get_final_price_distribution()
        stats = simulator.get_statistics()

        return JsonResponse(
            {
                "price_plot": price_plot,
                "distribution_plot": distribution_plot,
                "statistics": stats,
            }
        )

    return render(request, "monte_carlo_simulation.html")


def simulate_gbm_view(request):
    if request.method == "POST":
        S0 = float(request.POST.get("S0", 100))
        mu = float(request.POST.get("mu", 0.1))
        sigma = float(request.POST.get("sigma", 0.2))
        T = float(request.POST.get("T", 1))
        dt = float(request.POST.get("dt", 0.01))
        n_simulations = int(request.POST.get("n_simulations", 10))

        gbm = GeneralizedBrownianMotionUseCase(S0, mu, sigma, T, dt, n_simulations)
        time_grid, simulations = gbm.simulate_paths()
        price_plot = gbm.plot_paths(time_grid, simulations)
        distribution_plot = gbm.plot_distribution(simulations)
        stats = gbm.calculate_statistics(simulations)

        return JsonResponse(
            {
                "price_plot": price_plot,
                "distribution_plot": distribution_plot,
                "statistics": stats,
            }
        )

    return render(request, "simulate_gbm.html")


def simulate_mean_reversion_view(request):
    if request.method == "POST":
        S0 = float(request.POST.get("S0", 100))
        mu = float(request.POST.get("mu", 100))
        kappa = float(request.POST.get("kappa", 0.5))
        sigma = float(request.POST.get("sigma", 0.2))
        T = float(request.POST.get("T", 1))
        dt = float(request.POST.get("dt", 0.01))
        n_simulations = int(request.POST.get("n_simulations", 10))

        # Use case
        simulator = ReversaoMediaUseCase(S0, mu, kappa, sigma, T, dt, n_simulations)
        time_grid, simulations = simulator.simulate()
        paths_plot = simulator.plot_paths(time_grid, simulations)
        distribution_plot = simulator.plot_distribution(simulations)
        stats = simulator.calculate_statistics(simulations)

        return JsonResponse(
            {
                "paths_plot": paths_plot,
                "distribution_plot": distribution_plot,
                "statistics": stats,
            }
        )
    return render(request, "simulate_mean_reversion.html")
