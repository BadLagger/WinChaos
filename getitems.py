import requests
import pprint

items_req = requests.get('https://pathofexile.fandom.com/wiki/Body_Armour')
tab_list = items_req.text.split('\t\t\t\t')
print(type(tab_list))
print("Size: " + len(tab_list))


