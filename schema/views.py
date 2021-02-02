from django.shortcuts import render


def schema_view(request):

    return render(request, 'schema/schema.html')