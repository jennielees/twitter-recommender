from directed_edge import Exporter, Item, Database



class RecommendStore(object):
  def __init__(self):
    self.database = Database("project42startupweekend","878d9cedbec095d53f6904b5de855c74")
 
  def export_to_xml(self,users):
    exporter = Exporter('recommendstore.xml')
    # loop thru users and words
    k_exist = []
    for u in users:
      #pitem = Item(exporter.database,u.twitter)
      #pitem.add_tag('person')
      #exporter.export(pitem)
      for k in u.bio_kws:
        if k not in k_exist:
          item = Item(exporter.database,"k_%s" % k)
          item.add_tag('keyword')
          k_exist.append(k)
          exporter.export(item)

    #re-loop!!
    for u in users:
      pitem = Item(exporter.database,u.twitter)
      pitem.add_tag('person')
      for k in u.bio_kws:
        pitem.link_to("k_%s" % k)
      exporter.export(pitem)

    exporter.finish()

  def import_to_directed_edge(self):
    self.database.import_from_file('recommendstore.xml')




  def import_de_test(self):
    self.database.import_from_file('testrec.xml')

  def create_keyword(self,kw):
    item = Item(self.database,"k_%s" % kw)
    item.add_tag('keyword')
    item.save()

  def create_user(self,name):
    item = Item(self.database,name)
    item.add_tag('person')
    item.save()

  def add_bio(self,kw,name):
    item = Item(self.database,name)
    item.link_to("k_%s" % kw)
    item.save()

  def create_bio_links(self,user):
    for k in user.bio_kws:
      self.add_bio(k,user.twitter)

  def initialise_memory(self,users):
    for u in users:
      self.create_user(u.twitter)
      for k in u.bio_kws:
        self.create_keyword(k)
      self.create_bio_links(u)

  def recommend_peeps(self,username):
    item = Item(self.database,username)
    return item.related()

  def recommend_users(self,username):
    item = Item(self.database,username)
    return item.related(['person'],excludeLinked=True)



