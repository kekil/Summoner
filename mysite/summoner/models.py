from django.db import models

class Summoner(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class Match(models.Model):
    summoner = models.ForeignKey(Summoner)

    #champion played, number of kills, deaths and assists
    #for last match played
    champion = models.CharField(max_length=30)
    kills = models.CharField(max_length=2)
    deaths = models.CharField(max_length=2)
    assists = models.CharField(max_length=2)

    def __unicode(self):
        return self.champion
