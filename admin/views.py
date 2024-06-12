from django.shortcuts import render

def waver(request):
    return render(request, 'Admin/index.html', {})
