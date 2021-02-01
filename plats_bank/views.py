from django.shortcuts import render

from .forms import FindForm
from .models import Job_ad


# Create your views here.
def home_view(request):
    form = FindForm()
    city = request.POST['city']
    job_type = request.POST['job_type']
    qs = []
    print(city + "---" + job_type)
    if city or job_type:
        _filter = {}
        if city:
            _filter['city__id'] = city
        if job_type:
            _filter['job_type__id'] = job_type


    qs = Job_ad.objects.filter(**_filter)
    # qs = Job_ad.objects.filter(**_filter)
    print(qs)
    # qs = Job_ad.objects.all().order_by('-id')[:10]

    return render(request, 'plats_bank/home.html', {'object_list': qs, 'form': form})
