from summoner.models import Summoner
from django.shortcuts import render, get_object_or_404
import requests
from bs4 import BeautifulSoup

def home(request):
    soup = BeautifulSoup(requests.get("http://www.lolking.net/summoner/na/19907776#history").text)
    match = soup.find_all('div', {"class":"page_inner", "style":"position"}).find(id=1).find('div')
    match = match.find_all('div', {"class":"match_details_cell"})
    champion = match.find('a').get('href')
    print champion
    return render(request, 'summoner/home.html')

def index(request):
    latest_summoner_list = Summoner.objects.all().order_by('-name')[:10]
    context = { 'latest_summoner_list': latest_summoner_list}
    return render(request, 'summoner/index.html', context)

def detail(request, summoner_id):
    summoner = get_object_or_404(Summoner, pk=summoner_id)
    return render(request, 'summoner/detail.html', {'summoner':summoner})

