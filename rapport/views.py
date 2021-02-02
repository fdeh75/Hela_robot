from django.shortcuts import render


def rapport_view(request):
    return render(request, 'rapport/rapport.html')
