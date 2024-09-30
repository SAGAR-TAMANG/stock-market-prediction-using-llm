from django.shortcuts import render

# Create your views here.
def index(request):
  context = {
    'name': 'Upasana',
    'name_full': 'Upasana Das',
    'image':'upasana.jpg',
  }
  
  return render(request, 'index.html', context=context)