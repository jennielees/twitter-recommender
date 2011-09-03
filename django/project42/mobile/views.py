# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

from keywordpopulator import *
import twitter


def index(request):
    return render_to_response('index.html')


def recommendations(request, twittername):


  #TWITTER_ACCOUNT = "youshouldtalk"
    TWITTER_ACCOUNT = "festbuzz"
  #TWITTER_PASSWORD = "startupweekend"
    TWITTER_PASSWORD = "media6privy"



 ## get and check
    k = KeywordPopulator()
    users = k.populate()
    all = k.all
 
    #for u in users:
   #   print u.return_recommendations()
    u = users[0].find_person_in_list(twittername,users)
    if (u == None):
      return render_to_response('error.html')
    print u

    print u.twitter
    r = u.return_recommendations()

    # r list of usernames. get more data
    print r

    a = twitter.Api(username=TWITTER_ACCOUNT,password=TWITTER_PASSWORD)
    usrs = []
    for suggest in r:
      print "Recommending %s, checking friendship" % suggest
      if not a.FriendshipExists(twittername,suggest):
        usrs.append(a.GetUser(suggest)) 
    print usrs

    print "rah"
    return render_to_response('profiles.html', { 'recommendations': usrs })

def demo(request):
   # return recommendations(request,'jennielees')
    return render_to_response('jennielees.html')

def demo2(request):
    return render_to_response('chiprodgers.html')
