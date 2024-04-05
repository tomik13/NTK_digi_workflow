# pro veryi K5

import requests as rq
import os
import json


auth=("lysonekt","krameriusAdminTomik")


def check_upload_process_state(process_uuid):
    session = rq.session()

    params = {
        "uuid" : process_uuid
    }

    r = session.get("https://kramerius.techlib.cz/search/api/v4.6/processes", params=params, auth=auth)

    test = json.loads(r.content.decode())[0]
    state = test['state']
    batch_state = test['batchState']
    
    return state, batch_state

def check_uuid_inK5(uuid):
    res = rq.get('https://kramerius.techlib.cz/search/api/v5.0/item/uuid:'+uuid)
    return res.status_code

rootConvertDirecotory="/home/kramerius/.kramerius4/convert/"



def kramerius_import(stageFolder,defaultRights=False):
    s = rq.session()

    info = {
        "mapping": {
            "convertDirectory" : "/home/kramerius/.kramerius4/convert/",
            "convertTargetDirectory" : "/home/kramerius/.kramerius4/convert-converted",
            "ingestSkip" : False,
            "shutImageServer" : False,
            "startIndexer" : True,
            "defaultRights" : False
        }
    }    
    
    headers = {
        "Content-type" : "application/json"
    }


    data_dict = info.copy()
    mapping = data_dict["mapping"]
    mapping["convertDirectory"] = rootConvertDirecotory+stageFolder
    mapping["defaultRights"] = defaultRights
    
    data = json.dumps(data_dict)

    response = s.post("https://kramerius.techlib.cz/search/api/v4.6/processes?def=ndkmets", headers=headers, data=data, auth=auth)
    return json.loads(response.content)


input_directory = '/mnt/moon/DIGITALIZACE/EDITOR/kramerius_staging/'
import_directory = '/mnt/moon/DIGITALIZACE/EDITOR/kramerius_convert/'

def import_package_own_process(digi_info):
    urn = digi_info['urnnbn']
    stage_dir=f"stage_{urn}"
    stage_dir_path = os.path.join(import_directory,stage_dir)
    package_import_path = os.path.join(stage_dir_path,urn)
    package_path = digi_info['current_dir']

    os.mkdir(stage_dir_path)
    os.replace(package_path,package_import_path)
    digi_info['current_dir'] = package_import_path
    pc = kramerius_import(stage_dir,False)
    pcuuid = pc['uuid']
    digi_info['upload_uuid'] = pcuuid
    digi_info['upload_state'] = 'PLANNED'


def clear_import_stages():
    stages = os.listdir(import_directory)
    for stage in stages:
        if not os.listdir(pkg := os.path.join(import_directory,stage)):
            os.rmdir(pkg)



if __name__=='__main__':
    clear_import_stages()