from summoner.models import Summoner, Match
from django.shortcuts import render, get_object_or_404
from django import forms
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponseRedirect

def home(request):
    return render(request, 'summoner/home.html')

def index(request):
    latest_summoner_list = Summoner.objects.all().order_by('-name')[:10]
    context = { 'latest_summoner_list': latest_summoner_list}
    return render(request, 'summoner/index.html', context)

def detail(request, summoner_id):
    summoner = get_object_or_404(Summoner, pk=summoner_id)
    return render(request, 'summoner/detail.html', {'summoner':summoner})

def thanks(request):
    return render(request, 'summoner/thanks.html')

def getNumbers(s):
    return str(s.get_text()).split()[0]

def soup(request):
    r = requests.get("http://www.elophant.com/league-of-legends/summoner/na/19907776/recent-games")
    soup = BeautifulSoup(r.text)
    #grabs the most recent match information
    champion = soup.find('div', class_='title')
    kills = soup.find('div', class_='kills').find('span')
    deaths = soup.find('div', class_='deaths').find('span')
    assists = soup.find('div', class_='assists').find('span')
    #in format of <span> x Kills</span>, need to find x
    #change it to form of string from html, then split it to find x
    c = str(champion.get_text())
    k = getNumbers(kills)
    d = getNumbers(deaths)
    a = getNumbers(assists)
    s, created = Summoner.objects.get_or_create(name = 'CeciI')
    match = Match.objects.get_or_create(summoner = s, kills = k, deaths = d, assists = a, champion = c)
    return HttpResponseRedirect('/thanks/')

def create(request):
    if request.method == 'POST':
        form = SummonerForm(request.POST)
        if form.is_valid():
            newSummoner = form.cleaned_data['summoner']
            c = form.cleaned_data['champion']
            k = form.cleaned_data['kills']
            d = form.cleaned_data['deaths']
            a = form.cleaned_data['assists']
            newSummoner, created= Summoner.objects.get_or_create(name = newSummoner)
            match = Match.objects.create(summoner=newSummoner, champion=c, kills=k, assists=a, deaths=d)
            
            return HttpResponseRedirect('/thanks/')
    else:
        form = SummonerForm()
    return render(request, 'summoner/create.html', {'form':form,})

class SummonerForm(forms.Form):
    summoner = forms.CharField(max_length=30)
    champion = forms.CharField(max_length=30)
    kills = forms.CharField(max_length=2)
    deaths = forms.CharField(max_length=2)
    assists = forms.CharField(max_length=2)
