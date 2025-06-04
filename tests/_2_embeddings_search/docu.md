point name und point cond kombiniert in suche:
id: eval-Qv0-2025-06-04T13:15:16

```
def get_point_byquery(client, point, point_cond):
    coordinate = None
    if point_cond:
        res_cond = check_name(client, point_cond)
        coordinate = res_cond['coordinate'] if res_cond else None
        point_text = f'{point} {point_cond}'
    else:
        point_text = point
    res = check_name(client, point_text, coordinate=coordinate)
    if res:
        res2 = {}
        res2['location'] = res['coordinate']
        res2['name'] = res['name']
        return res2
    return None
```

schlechter als nur point name in suche:
id: eval-GXd-2025-06-04T13:12:46

```
def get_point_byquery(client, point, point_cond):
    coordinate = None
    if point_cond:
        res_cond = check_name(client, point_cond)
        coordinate = res_cond['coordinate'] if res_cond else None
    res = check_name(client, point, coordinate=coordinate)
    if res:
        res2 = {}
        res2['location'] = res['coordinate']
        res2['name'] = res['name']
        return res2
    return None
```

---
