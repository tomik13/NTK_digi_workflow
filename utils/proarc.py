import requests as rq
import json

# login = {
#     'j_username' : 'robot',
#     'j_password' : 'robotAuto'
# }


logins = {
    'proarc': {
        'j_username' : 'proarc',
        'j_password' : 'proarcAdmin'
    },
    'robot' : {
        'j_username' : 'robot',
        'j_password' : 'robotAuto'
    },
    'malaj' : {
        'j_username' : 'malaj',
        'j_password' : 'mjDigi'
    }
}


proarcBaseUrl = 'http://digi-workflow.ntkcz.cz:8080/proarc/'
proarcApiBase = proarcBaseUrl+'rest/v1/'
proarcLoginUrl= proarcBaseUrl+'proarclogin'

def make_year(parent, date, number, session = None):

    s = session if session else rq.session()
    s.post(proarcLoginUrl, params=logins['robot'])

    q = {
        'model': 'model:ndkperiodicalvolume',
        'parent': parent,
        '_operationType': 'add',
        '_textMatchStyle': 'exact',
        '_dataSource': 'DigitalObjectDataSource',
        'isc_metaDataPrefix': '_',
        'isc_dataFormat': 'json'
    }

    h = {
        'Content-type' : 'application/x-www-form-urlencoded'
    }

    r = s.post(proarcApiBase+'object', params=q, headers=h)

    j = json.loads(r.content.decode())

    newuuid = j['response']['data'][0]["pid"]

    q = {
        'editorId': 'model:ndkperiodicalissue',
        'pid': newuuid,
        '_operationType': 'fetch',
        '_textMatchStyle': 'exact',
        '_dataSource': 'ModsCustomDataSource',
        'isc_metaDataPrefix': '_',
        'isc_dataFormat': 'json'
    }

    r = s.get(proarcApiBase+'object/mods/custom', headers=h, params=q)

    j2 = json.loads(r.content.decode())

    timestamp = j2["response"]["data"][0]["timestamp"]

    data = j2["response"]["data"][0]["jsonData"]["mods"]
    data["originInfo"] = [
        {
            "dateIssued" : {"value" : str(date)}
        }
    ]
    if "titleInfo" in data:
        data["titleInfo"][0]["partNumber"] = {
            "value" : str(number)
        }
    else:
        data["titleInfo"] = [{
            "partNumber" : {
                "value" : str(number)
                }
            }]

    jData = {"mods" : data}

    q = {
        'pid': newuuid,
        'timestamp': timestamp,
        'editorId': 'model:ndkperiodicalissue',
        'jsonData': json.dumps(jData),
        '_operationType': 'update',
        '_textMatchStyle': 'exact',
        '_dataSource': 'ModsCustomDataSource',
        'isc_metaDataPrefix': '_',
        'isc_dataFormat': 'json'
    }

    r = s.put(proarcApiBase+'object/mods/custom',headers=h,params=q)

    print(r.content)

    return newuuid


def make_issue(parent, date, number, session = None):
    
    s = session if session else rq.session()
    s.post(proarcLoginUrl, params=logins['robot'])

    q = {
        'model': 'model:ndkperiodicalissue',
        'parent': parent,
        '_operationType': 'add',
        '_textMatchStyle': 'exact',
        '_dataSource': 'DigitalObjectDataSource',
        'isc_metaDataPrefix': '_',
        'isc_dataFormat': 'json'
    }

    h = {
        'Content-type' : 'application/x-www-form-urlencoded'
    }

    r = s.post(proarcApiBase+'object', params=q, headers=h)

    j = json.loads(r.content.decode())

    newuuid = j['response']['data'][0]["pid"]

    q = {
        'editorId': 'model:ndkperiodicalissue',
        'pid': newuuid,
        '_operationType': 'fetch',
        '_textMatchStyle': 'exact',
        '_dataSource': 'ModsCustomDataSource',
        'isc_metaDataPrefix': '_',
        'isc_dataFormat': 'json'
    }

    r = s.get(proarcApiBase+'object/mods/custom', headers=h, params=q)

    j2 = json.loads(r.content.decode())

    timestamp = j2["response"]["data"][0]["timestamp"]

    data = j2["response"]["data"][0]["jsonData"]["mods"]
    data["originInfo"] = [
        {
            "dateIssued" : {"value" : str(date)}
        }
    ]
    data["titleInfo"][0]["partNumber"] = {
        "value" : str(number)
    }

    jData = {"mods" : data}

    q = {
        'pid': newuuid,
        'timestamp': timestamp,
        'editorId': 'model:ndkperiodicalissue',
        'jsonData': json.dumps(jData),
        '_operationType': 'update',
        '_textMatchStyle': 'exact',
        '_dataSource': 'ModsCustomDataSource',
        'isc_metaDataPrefix': '_',
        'isc_dataFormat': 'json'
    }

    r = s.put(proarcApiBase+'object/mods/custom',headers=h,params=q)

    print(r.content)

    return newuuid



## Vytvoreni nekolika rocniku Sdelovaci Techniky po dvanacti cislech. Jelikoz mame dobrou praxi pri pojmenovani slozek s cisly periodik, bylo by asi mozne vatvaret cisla periodik automaticky a cist udaje z nazvu. Pripadne si umim zaindexovat spravna uuid v nejakem souboru.

# parentuuid = "uuid:87a0347e-c080-4743-9d91-edf4eace6f32"

# for i in range(66,67):
#     year = 1952 + i
#     volume_uuid = make_year(parentuuid, year, i)
#     print('volume:', volume_uuid)
#     for j in range(1,13):
#         if j not in [7,8,11,12]:
#             issue_uuid = make_issue(volume_uuid, year, j)
#             print('issue:', issue_uuid)
#         if j == 7 or j == 11:
#             issue_uuid = make_issue(volume_uuid, year, str(j)+','+str(j+1))
#             print('issue:', issue_uuid)


devices = {
    'oldprints/EOD' : 'device:e4245c00-183a-48d8-b9da-a7a6460f299d'
}

def start_import(path,device,user):
    data = {
        'folderPath' : path,
        'profile' : 'profile.default',
        'indices' : 'true',
        'device' : devices[device],
        '_operationType': 'add',
        '_textMatchStyle': 'exact',
        '_dataSource': 'ImportBatchDataSource',
        'isc_metaDataPrefix': '_',
        'isc_dataFormat': 'json'
    }

    h = {
        'Content-type' : 'application/x-www-form-urlencoded'
    }

    s = rq.session()
    s.post(proarcLoginUrl, params=logins[user])

    r = s.post(proarcApiBase+'import/batch', params=data, headers=h)

    print(r.status_code)



