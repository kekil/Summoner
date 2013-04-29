from summoner.models import Summoner, Match
from django.shortcuts import render, get_object_or_404
from django import forms
from django.forms.widgets import RadioSelect
from django.forms.fields import ChoiceField
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponseRedirect, HttpResponse

def home(request):
    return render(request, 'summoner/home.html')

def index(request):
    latest_summoner_list = Summoner.objects.all().order_by('-name')[:10]
    context = { 'latest_summoner_list': latest_summoner_list}
    return render(request, 'summoner/index.html', context)
def search_index(request):
    if 's' in request.GET:
        summonerName = request.GET['s'] 
        summoner = Summoner.objects.filter(name=summonerName)
        context = {'summoner':summoner, 'search':summonerName}
    #return HttpResponseRedirect('/search_index/', context)
        return render(request, 'summoner/search_index.html', context)
    else:
        return render(request, 'home.html', {'error':True})

def detail(request, summoner_id):
    summoner = get_object_or_404(Summoner, pk=summoner_id)
    return render(request, 'summoner/detail.html', {'summoner':summoner})

def about(request):
    return render(request, 'summoner/about.html')

def thanks(request):
    return render(request, 'summoner/thanks.html')

def getNumbers(s):
    #in form <span> x kills </span>, grabs the x
    return str(s.get_text()).split()[0]

def soup(request):
    profilepage = "http://www.elophant.com/league-of-legends/summoner/na/19907776/recent-games"
    getSummonerMatchHistory(profilepage, 'CeciI')
    return HttpResponseRedirect('/thanks/')

def superSoup(request):
    if request.method == 'POST':
        form = SoupForm(request.POST)
        if form.is_valid():
            searchString = "http://www.elophant.com/league-of-legends/search?query="
            newSummoner = form.cleaned_data['summoner']
            #flag corresponds to Yes No Radio Buttons
            flag = False
            if form.cleaned_data['All_Summoners']=='1':
                flag = True
            newSearch = searchString + newSummoner
            soup = BeautifulSoup(requests.get(newSearch).text)
            sprofile = soup.find('div', class_='alter search-results').find('a').get('href')
            profilepage = "http://www.elophant.com" + str(sprofile) + "/recent-games"
            getSummonerMatchHistory(profilepage, newSummoner)
            if (flag):
                soup = BeautifulSoup(requests.get(profilepage).text)
                #gets list of summoners information in the most recent game
                blue = soup.find('div', class_='team blue').find_all('a')
                red = soup.find('div', class_='team red').find_all('a')
                
                blueTeam = getTeamInfo(blue)
                redTeam = getTeamInfo(red)

                for a, b in blueTeam:
                    summonerProfile = str("http://www.elophant.com"+a+"/recent-games")
                    getSummonerMatchHistory(summonerProfile, b)
                #handles if the game is a coop vs ai (bot games)
                if len(redTeam)>0:
                    for a,b in redTeam:
                        summonerProfile = "http://www.elophant.com"+a+"/recent-games"
                        getSummonerMatchHistory(summonerProfile, b)

            return HttpResponseRedirect('/thanks/')
    else:
        form = SoupForm()
    return render(request, 'summoner/superSoup.html', {'form':form,})
            
def getTeamInfo(team):
    teamSummonerUrls = [x.get('href') for x in team]
    teamSummonerUrls = [x for x in teamSummonerUrls if 'summoner' in x] 
    teamSummonerNames = [x.get_text() for x in team]
    teamSummonerNames = [x for x in teamSummonerNames if x != '']
    return zip(teamSummonerUrls, teamSummonerNames)

def getSummonerMatchHistory(profilepage, summonerName):
    soup = BeautifulSoup(requests.get(profilepage).text)
    #grabs the most recent match information
    champion = soup.find_all('div', class_='title')
    kills = soup.find_all('div', class_='kills')
    deaths = soup.find_all('div', class_='deaths')
    assists = soup.find_all('div', class_='assists')

    #narrows each respective info down to the span information
    kills = [x.find('span') for x in kills]
    kills = [x for x in kills if x != None]
    deaths = [x.find('span') for x in deaths]
    deaths = [x for x in deaths if x != None]
    assists = [x.find('span') for x in assists]
    assists = [x for x in assists if x != None]

    for c, k, d, a in zip(champion, kills, deaths, assists):
        c = str(c.get_text())
        k = getNumbers(k)
        d = getNumbers(d)
        a = getNumbers(a)
        s, created = Summoner.objects.get_or_create(name = summonerName)
        match = Match.objects.get_or_create(summoner = s, kills = k, deaths = d, assists = a, champion = c)

class SoupForm(forms.Form):
    summoner = forms.CharField(max_length=30)
    yesNo = ( (1, 'Yes'),
        (0, 'No'), )
    All_Summoners = forms.ChoiceField(widget=forms.RadioSelect, choices=yesNo)

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
