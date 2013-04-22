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
    champion = soup.find_all('div', class_='title')
    kills = soup.find_all('div', class_='kills')
    deaths = soup.find_all('div', class_='deaths')
    assists = soup.find_all('div', class_='assists')
    for x in range(0, len(kills)-1):
        kills[x] = kills[x].find('span')
        deaths[x] = deaths[x].find('span')
        assists[x] = assists[x].find('span')
    for a, b, c in zip(kills, deaths, assists):
        if a == None: 
            kills.remove(a)
        if b == None:
            deaths.remove(b)
        if c == None:
            assists.remove(c)
    kills.remove(kills[len(kills)-1])
    deaths.remove(deaths[len(deaths)-1])
    assists.remove(assists[len(assists)-1])
    print kills, deaths, assists
    #in format of <span> x Kills</span>, need to find x
    #change it to form of string from html, then split it to find x
    for c, k, d, a in zip(champion, kills, deaths, assists):
        c = str(c.get_text())
        k = getNumbers(k)
        d = getNumbers(d)
        a = getNumbers(a)
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
