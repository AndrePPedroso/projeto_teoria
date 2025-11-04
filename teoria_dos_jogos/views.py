from django.shortcuts import render
from django.http import JsonResponse
from .use_cases.dilema_prisioneiro_use_case import DilemaPrisioneiroUseCase

def dilema_do_prisioneiro_view(request):
    if request.method == 'POST':
        strategy1 = request.POST.get('strategy1', 'always_cooperate')
        strategy2 = request.POST.get('strategy2', 'always_cooperate')
        iterations = int(request.POST.get('iterations', 10))

        use_case = DilemaPrisioneiroUseCase(strategy1, strategy2, iterations)
        result = use_case.run_simulation()

        context = {
            'result': result,
            'strategy1': strategy1,
            'strategy2': strategy2,
            'iterations': iterations,
        }
        return JsonResponse(context)

    return render(request, 'site/teoria_dos_jogos/dilema_prisioneiro.html')