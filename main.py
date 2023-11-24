import requests
import tablib
import os
import json


def send_request():
      worldurl = get_worldurl()
      keys = get_keys(worldurl)
      request = requests.get(f"https://{worldurl}/api/external.php?action=getMapData&privateApiKey={keys["privateApiKey"]}")
      kingdoms = get_kingdoms(request)
      kingdom_id = get_kingdom_id(kingdoms)
      players = get_players(request)
      cells = get_cells(request)
      chosen_players = dict()
      for player in players:
            if player["kingdomId"] == kingdom_id:
                  role = get_role(player)
                  chosen_players[player["playerId"]] = list()
                  for i in player["villages"]:
                        restype = get_restype(i["x"], i["y"], cells)
                        chosen_players[player["playerId"]].append({
                              "Role" : role,
                              "Player Name" : player["name"],
                              "Village Name" : i["name"],
                              "X" : i["x"],
                              "Y" : i["y"],
                              "Population" : i["population"],
                              "Capital" : i["isMainVillage"],
                              "ResType": restype,
                              "City" : i["isCity"],
                              "Player ID" : player["playerId"],
                              "Village ID": i["villageId"]
                  })

      data = tablib.Dataset(headers=['Role', 'Player Name', 'Village Name', 'X', 'Y', 'Population', 'Capital', 'ResType', 'City', 'Player ID', 'Village ID'])
      for values in chosen_players.values():
            for datas in values:
                  data.append(datas.values())
      with open('output.xlsx', 'wb') as f:
            f.write(data.export('xlsx'))

def get_worldurl():
      if os.path.isfile("world.json"):
            try:
                  f = open("world.json")
                  data = json.load(f)
                  worldurl = data["worldurl"]
                  f.close()
            except:
                  f.close()
                  os.remove("world.json")
                  worldurl = input("Enter the kingdom worldurl [for example: com2.kingdoms.com]:")
      else:
            worldurl = input("Enter the kingdom worldurl [for example: com2.kingdoms.com]:")
            with open("world.json", "w") as outfile:
                  outfile.write("{")
                  outfile.write(f"\"worldurl\" : \"{worldurl}\"")
                  outfile.write("}")
      return worldurl

def get_keys(worldurl):
      keys = requests.get(f"https://{worldurl}/api/external.php?action=requestApiKey&email=jatekalex@gmail.com&siteName=google&siteUrl=https://www.google.com/&public=false")
      return {
            "privateApiKey" : keys.json()["response"]["privateApiKey"],
            "publicSiteKey" : keys.json()["response"]["publicSiteKey"]
      }

def get_kingdoms(request):
      return request.json()["response"]["kingdoms"]

def get_kingdom_id(kingdoms):
      kingdom_name = get_kingdom_name()
      for kingdom in kingdoms:
            if kingdom["kingdomTag"].lower() == kingdom_name.lower():
                  return kingdom["kingdomId"]

def get_kingdom_name():
      kingdom_name = input("Enter the kingdom name:")
      return kingdom_name

def get_players(request):
      return request.json()["response"]["players"]

def get_cells(request):
      return request.json()["response"]["map"]["cells"]

def get_role(player):
      match player["role"]:
            case 0:
                  return "Governor"
            case 1:
                  return "King"
            case 2:
                  return "Duke"
            case 3:
                  return "ViceKing"

def get_restype(currentX, currentY, cells):
      for mapRes in cells:
            if mapRes["x"] == currentX and mapRes["y"] == currentY:
                  return mapRes["resType"]

def main():
      send_request()

if __name__ == "__main__":
      main()
