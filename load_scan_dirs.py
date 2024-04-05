import os
import re
import json

from utils.aleph import aleph_dict_ids



def parse_directory(path, preset = None):
    if preset:
        info = preset.copy()
    else:
        info = {}
    
    dirname = os.path.basename(path)

    info['dir_name'] = dirname
    info['original_dir'] = path


    # callnumber with maybe a volume and maybe an item identifier
    regexCallnoSysno=r"^([A-Z]{0,2})[_ ]?([0-9]+)(?:[-_]([0-9IV]{0,8})?)?([a-z])?(?:_([0-9]{9}))?$"
    regexCallnoSysnoVISK=r"^([A-Z]{0,2})[_ ]?([0-9]+)[a-z_ ]+([0-9]+)$"
    regexSysno=r"^([0-9]{9})$"
    regexSTK=r"^STK_+([A-Z]+)([0-9]+)SYS.*$"
    regexEOD=r"^(NTK[0-9]{2}A[0-9]{6})_([0-9]{9})$"
    regexPeriodical=r"^([0-9]{9})_([0-9]{4}(?:_[0-9]{4})?)_([0-9]{2})_([0-9]{2}(?:_[0-9]{2})?)$"

    if result := re.search(regexSysno, dirname):
        info['sysno'] = result.group(1)
    elif result := re.search(regexCallnoSysno, dirname):
        # print(result.groups())
    
        capital = result.group(1)
        num = result.group(2)
        slash = result.group(3)
        info['letter'] = result.group(4)
        info['sysno'] = result.group(5)
        info['callno'] = (capital+" " if capital else "")+num+("/"+slash if slash else "")
    elif result := re.search(regexSTK, dirname):
        capital = result.group(1)
        num = result.group(2)
        info['callno'] = capital + ' ' + num
        info['sysno'] = None
    elif result := re.search(regexCallnoSysnoVISK, dirname):
        capital = result.group(1)
        num = result.group(2)
        info['callno'] = capital + ' ' + num
        sysno_old = result.group(3)
        info['sysno'] = 'sysno_old'.zfill(9)
    elif result := re.search(regexEOD, dirname):
        info['EOD_num'] = result.group(1)
        info['sysno'] = result.group(2)
        info['fin'] = 'eod'
    elif result := re.search(regexPeriodical, dirname):
        info['sysno'] = result.group(1)
        info['year'] = result.group(2)
        info['volume'] = result.group(3)
        info['issue'] = result.group(4)
        info['type'] = 'SE'
    else:
        pass

    return info


def resolve_callno(callno,letter=""):
    letter = letter if letter else ""
    regex_cn= r"^([0-9]{9}).*\$\$b("+callno+r"(?: "+letter+r")?)(?:\$\$.*)?$"
    with open('utils/jk_pole_910_all.txt','rt') as callnos:
        while not ((line := callnos.readline()) == '' or (res := re.match(regex_cn, line))): pass
    
    return res.group(1) if res else None


def make_info_of_path(path, preset = None):
    info = parse_directory(path, preset)
    info['problems'] = []

    if not info.get('callno') and not info.get('sysno'):
        info['problems'].append('Failed to resolve callno or sysno')
        return info

    if not info.get('sysno'):
        info['sysno'] = resolve_callno(info.get('callno'),info.get('letter'))
    
    if not info.get('sysno'):
        info['problems'].append('Failed to resolve system number')
        return info
    

    d = aleph_dict_ids(info['sysno'])

    info['catalog_data'] = d

    if info.get('type') == 'SE':
        info['NTK_digi_id'] = f"{info['sysno']}_{info['volume']}_{info['issue']}"
    else:
        info['NTK_digi_id'] = f"{info['sysno']}"

    return info

loaded_scan_path = '/mnt/moon/DIGITALIZACE/WORKFLOW_TEST/loaded_scans'
problem_scan_path = '/mnt/moon/DIGITALIZACE/WORKFLOW_TEST/problematic_scans'

def load_scan_directory(path,preset = None):
    digi_info = make_info_of_path(path, preset)
    if not digi_info['problems']:
        new_dir = os.path.join(loaded_scan_path,digi_info['dir_name'])
    else:
        new_dir = os.path.join(problem_scan_path,digi_info['dir_name'])
    os.replace(digi_info['original_dir'],new_dir)
    digi_info['current_dir'] = new_dir

    return digi_info



scan_import_directory = '/mnt/moon/DIGITALIZACE/WORKFLOW_TEST/new_scans'

def load_scan_dirs():
    # udeleje seznam slozek v importnim adresari
    dirs = os.listdir(scan_import_directory)
    print(dirs)
    profiles = [d for d in dirs if 'profile_' in d]
    scan_dirs = [d for d in dirs if not 'profile_' in d]

    control_list = []


    for dir in scan_dirs:
        control_list.append(load_scan_directory(os.path.join(scan_import_directory,dir)))

    for profile in profiles:
        profile_path = os.path.join(scan_import_directory,profile)
        preset_path = os.path.join(profile_path,'preset.json')
        if os.path.exists(preset_path):
            with open(preset_path,'rt') as f:
                preset = json.load(f)
        else:
            preset = {}
        dirs = os.listdir(profile_path)
        for dir in dirs:
            if os.path.isdir(os.path.join(profile_path,dir)):
                control_list.append(load_scan_directory(os.path.join(profile_path,dir),preset))
        

    return control_list
    