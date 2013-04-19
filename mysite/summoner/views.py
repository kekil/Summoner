from summoner.models import Summoner
from django.shortcuts import render, get_object_or_404

def home(request):
    return render(request, 'summoner/home.html')

def index(request):
    latest_summoner_list = Summoner.objects.all().order_by('-name')[:10]
    context = { 'latest_summoner_list': latest_summoner_list}
    return render(request, 'summoner/index.html', context)

def detail(request, summoner_id):
    summoner = get_object_or_404(Summoner, pk=summoner_id)
    return render(request, 'summoner/detail.html', {'summoner':summoner})

