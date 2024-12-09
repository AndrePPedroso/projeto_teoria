from django.shortcuts import render

def volatilidade_template(request):
    return render(request, 'site/teoria/volatilidade.html')
