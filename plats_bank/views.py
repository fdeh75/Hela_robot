from django.shortcuts import render
from django.core.paginator import Paginator

from .form import FindForm
from .models import Job_ad


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    job_type = request.GET.get('job_type')
    page_obj = []
    _context = {'city': city, 'job_type': job_type, 'form': form}
    if city or job_type:
        _filter = {}
        if city:
            _filter['city__id'] = city
        if job_type:
            _filter['job_type__id'] = job_type

        qs = Job_ad.objects.filter(**_filter)
        paginator = Paginator(qs, 9)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        _context['object_list'] = page_obj

    return render(request, 'plats_bank/list.html', _context)
