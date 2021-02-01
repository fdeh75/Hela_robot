from django.shortcuts import render

from plats_bank.forms import FindForm


def home(request):
    form = FindForm()
    return render(request, 'plats_bank/home.html', {'form': form})

 # def home_view(request):
 #     form = FindForm()
 #     return render(request, 'plats_bank/home.html', {'form': form})