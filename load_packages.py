# functions for loading packages from the designated import directory
import os
import json

from utils.kramerius import check_uuid_inK5,check_upload_process_state
from utils.NDK_mets import mine_mets
from update_statuses import update_aleph_link

import config


with open('/mnt/moon/DIGITALIZACE/WORKFLOW_TEST/data/NTK_001-SYSNO_fix', 'rt') as f:
    fix001 = json.load(f)

def update_kramerius_status(digi_info):
        itemuuid = digi_info['item']
        if (k5status := check_uuid_inK5(itemuuid)) == 404:
            digi_info['kramerius'] = False
        elif k5status == 200:
            digi_info['kramerius'] = True
        else:
            raise Exception('some bs with checking kramerius state')

def update_kramerius_upload_process_status(digi_info):
    process_uuid = digi_info.get('upload_uuid')
    if not process_uuid: return
    state, batch_state = check_upload_process_state(process_uuid)
        
    print(state, batch_state)
    if state == "FINISHED":
        digi_info['upload_state'] = batch_state
    else:
        digi_info['upload_state'] = state

    if digi_info['upload_state'] == 'BATCH_FINISHED':
        digi_info['kramerius'] = True

# import_directory = '/mnt/moon/DIGITALIZACE/WORKFLOW_TEST/new_exports/'
# loaded_directory = '/mnt/moon/DIGITALIZACE/WORKFLOW_TEST/loaded/'

def load_package(path):
    pkg = mine_mets(os.path.join(path))
    urn = os.path.basename(path)
    rootuuid = pkg[pkg['root']]['uuid'][0]
    itemuuid = pkg[pkg['tail']]['uuid'][0]
    year = pkg[pkg['tail']]['date'][0]
    FMT = 'BK'

    print(pkg)

    volume, issue = None,None
    if 'periodical' in pkg[pkg['root']]['model'][0]:
        FMT = 'SE'
        volume = f"{pkg['MODSMD_VOLUME_0001']['number'][0]:>02}"
        issue = f"{pkg[pkg['tail']]['number'][0]:>02}"
    year = int(year.strip('[]').split('.')[-1])
    if year <= 1800:
        FMT = 'RP'
    print(year)

    root001 = pkg[pkg['root']]['rec_sysno'][0]
    rootsysno = fix001[root001] if root001 in fix001 else root001

    newpath = os.path.join(config.NDK_loaded_directory,urn)
    os.replace(path,newpath)

    digi_info = {
        'urnnbn' : urn,
        'root' : rootuuid,
        'item' : itemuuid,
        'sysno' : rootsysno,
        '001' : root001,
        'import_dir' : path,
        'current_dir' : newpath,
        'year' : year,
        'FMT' : FMT,
        'digi_stage': 0,
        'NTK_digi_id' : f"{rootsysno}{'_'+volume if volume else ''}{'_'+issue if issue else ''}"
    }


    print(rootuuid,itemuuid, rootsysno)

    update_kramerius_status(digi_info)
    update_aleph_link(digi_info)

    return digi_info

def load_packages():
    # udeleje seznam slozek v importnim adresari
    package_list = os.listdir(config.NDK_input_directory)
    print(package_list)

    control_dict = {}

    for urn in package_list:
        control_dict[urn] = load_package(os.path.join(config.NDK_input_directory,urn))

    return control_dict


if __name__ == '__main__':
    infos = load_packages()
    with open('testfiles/pokus2','wt') as f:
        json.dump(infos,f,indent=4)