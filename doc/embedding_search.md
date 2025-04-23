## probleme bei geofox

zunächst wird nach altona gesucht:
```sdName = {
"type": "UNKNOWN",
"name": "Norderstedt",
"city": "Hamburg",
}
res2 = check_name(client, sdName)
res2```

```{'returnCode': 'OK',
 'results': [{'name': 'ZOB',
   'city': 'Glashütte',
   'combinedName': 'Glashütte, ZOB',
   'id': 'Master:92021',
   'globalId': 'de:01060:92021',
   'type': 'STATION',
   'coordinate': {'x': 10.037496, 'y': 53.688677},```

danach park in nähe von Norderstedt:
```sdName = {
"type": "UNKNOWN",
"name": "park",
"city": "Hamburg",
"coordinate": {'x': 10.037496, 'y': 53.688677}
}
res2 = check_name(client, sdName)
res2```

```{'returnCode': 'OK',
 'results': [{'name': 'Botanischer Garten Alt',
   'city': 'Hamburg',
   'combinedName': 'Botanischer Garten Alt',
   'id': '205001',
   'type': 'POI',
   'coordinate': {'x': 9.985986, 'y': 53.559203},
   'address': 'Stephansplatz (Hamburg)'},```

-> resultat ist weit von norderstedt entfernt 