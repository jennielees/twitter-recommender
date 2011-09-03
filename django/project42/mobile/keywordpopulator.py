#!/usr/bin/python

import nltk
import twitter
import itertools
import re
import networkx as nx
from recommendstore import RecommendStore
import y_serial_v052 as y_serial
from directed_edge import Exporter, Item, Database
from persondata import DataImport

class Intent():
  entities = ""
  direction = ""
  keyword_string = ""
  def __init__(self, kw):
    self.keyword_string = kw

class Person():
  twitter = ""
  user_image_url = ""
  user_name = ""
  bio_kws = []
  recommends = {}

  def set_name(self,name):
    self.user_name = name
  
  def set_image_url(self,url):
    self.user_image_url = url

  def save(self,ys):
    ys.insert(self,self.twitter,'people')
  
  def find_person_in_list(self,key,list):
    for u in list:
      if u.twitter == key:
        return u

  def add_likeminded(self,userlist,reason):
    for u in userlist:
      if u is not self.twitter:
        # check for rec
        if u in self.recommends.keys():
          self.recommends[u] += 1
        else:
          self.recommends[u] = 1 
  
  def clear_recommendations(self):
    self.recommends = {}

  def return_recommendations(self):
    sr =  sorted(self.recommends.items(), key=lambda(k,v): v,reverse=True)
    return [s[0] for s in sr]

  def __init__(self, twid, kws):
    self.bio_kws = kws
    self.twitter = twid

class GraphStore():

  def save(self):
    nx.write_yaml(self.graph,'graph.yaml')
  
  def shortest_path(self,fromnode,tonode):
    return nx.shortest_path(self.graph,fromnode,tonode)

  def open(self):
    self.graph = nx.read_yaml('graph.yaml')

  def create_graph(self,users):
    self.initialise_memory(users)

  def create_keyword(self,kw):
    self.graph.add_node(kw)

  def create_user(self,name):
    self.graph.add_node(name)

  def add_bio(self,kw,name):
    self.graph.add_edge(name,kw)

  def create_bio_links(self,user):
    for k in user.bio_kws:
      self.graph.add_edge(user.twitter,k)

  def initialise_memory(self,users):
    self.graph.add_nodes_from([x.twitter for x in users],tag='person')
    for u in users: 
      for k in u.bio_kws:
        self.graph.add_nodes_from(k,tag='k')
        self.graph.add_edge(u.twitter,k,tag='t')

  def find_others_by_name(self,twittername,allusers):
    u = allusers[0].find_user_in_list(twittername,allusers) 
    return find_others(self,u,allusers)

  def find_others(self,user,allusers):
    user.clear_recommendations()
    for x in self.graph.neighbors_iter(user.twitter):
      if x not in [u.twitter for u in allusers]:
        # if it isnt another user (currently breaks graph)
        user.add_likeminded(self.graph.neighbors(x),x)
    # Why returning multiple types
    return user.return_recommendations()

  def __init__(self):
    self.graph = nx.Graph()


class KeywordPopulator():

  peeps = []
  def populate(self):

   # STOP = open('stopwords.txt')
   # stopwords = []
  #for s in STOP.readlines():
 #   stopwords.append(s.rstrip())
 # STOP.close()
 
    EXAMPLE_LOOKING = "social media guru hacker"

    EXAMPLE_TAG = "swbay"


  #TWITTER_ACCOUNT = "youshouldtalk"
    TWITTER_ACCOUNT = "festbuzz"
  #TWITTER_PASSWORD = "startupweekend"
    TWITTER_PASSWORD = "media6privy"


    store = y_serial.Main('sqlite.sql')

# Keyword extraction on looking-for (TODO semantic rep)

    i = Intent(EXAMPLE_LOOKING)
    i.keywords = nltk.word_tokenize(i.keyword_string)

# TODO
# Named entity



# Get matching tweets [ we gotta get attendees somehow ]

    a = twitter.Api(username=TWITTER_ACCOUNT,password=TWITTER_PASSWORD)

# Get attendees
    attendees = []

    page = 1 
    while (page<5):
      tweets = a.Search(EXAMPLE_TAG,page=page)
      for t in tweets:
        attendees.append(t.user.screen_name)
      page += 1


    attendees = list(set(attendees))

# Get bios of attendees
    peeps = []

    stemmer = nltk.stem.porter.PorterStemmer()
    for p in attendees:
      try:
        isp = store.select(p,'people')
      except IOError:
        isp = None
      if isp == None:
        u = a.GetUser(p)

        if u.description:
          sent = nltk.sent_tokenize(u.description)
          word = [nltk.word_tokenize(s) for s in sent]
          sent = [nltk.pos_tag(s) for s in word]
          s = list(itertools.chain(*sent))

          match_regexp = "NN(P)?|JJ"
	  desc_tok = []
          for (word,postag) in s:
            if re.search(match_regexp,postag):
              desc_tok.append(word.lower()) 
              desc_tok.append(stemmer.stem(word.lower()))

          #desc_tok = [w.lower().rstrip(":,.") for w in nltk.word_tokenize(u.description) if w not in stopwords and len(w)>3]
        else:
          desc_tok = ""
        p = Person(p, desc_tok)
        p.set_name(u.name)
        p.set_image_url(u.profile_image_url)
        p.save(store)
        peeps.append(p)
      else:
        peeps.append(isp)
  

  #j = peeps[0].find_person_in_list('jennielees',peeps)


    all_attendees = store.selectdic('','people')
    all_attendees = [x[1][2] for x in all_attendees.items()]

    g = GraphStore()
    g.initialise_memory(peeps) 
    g.initialise_memory(all_attendees)
    g.save()

    print "Graph initialised"
   # for j in peeps:
   #   #print "\nRecs for %s\n" % j.twitter
    #  recs = g.find_others(j,all_attendees)
    #  j.save(store)

    print "Attendees saved"
    #for r in recs:
     # Does the friendship exist?
    # if not a.FriendshipExists(j.twitter,r[0]):

    #   print r[0]
    #   print "Recommended because you both like %s" % g.shortest_path(j.twitter,r[0])[1]
  
     #else:
     #  print "Already following %s" % r[0]

  # Spit out html files!
  
    self.graph = g
    self.peeps = peeps
    self.all = all_attendees
    return peeps

  def get_recs_for(self,twittername):
    recs = self.graph.find_others_by_name(twittername,self.all)
    return recs 


# Check for matches

 # r = RecommendStore()

 # r.export_to_xml(peeps)
 # r.import_to_directed_edge()
 # r.initialise_memory(peeps)

 # print r.recommend_peeps(peeps[0].twitter)
 # print r.recommend_peeps('jennielees')
