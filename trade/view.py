from django.shortcuts import render


def index(request):
    context = {}
    context['hello'] = 'Hello World!11111'
    return render(request, 'index.html', context)
