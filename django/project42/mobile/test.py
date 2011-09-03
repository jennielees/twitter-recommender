from keywordpopulator import *

k = KeywordPopulator()
users = k.populate()

for u in users:
  print u.return_recommendations()
