import os
from utils.proarc import start_import

proarc_home = '/mnt/moon/DIGITALIZACE/EDITOR'

def start_import_scans(scan_info):
    user = u if (u:=scan_info.get('user')) else 'proarc'
    scan_info['user'] = user
    project = p if (p:=scan_info.get('project')) else 'TESTY'
    user_dir = os.path.join(proarc_home,user)
    project_dir = os.path.join(user_dir,'import',project)
    if not os.path.exists(project_dir):
        os.mkdir(project_dir)
    new_path = os.path.join(project_dir,scan_info['dir_name'])
    current = scan_info['current_dir']
    
    os.replace(current,new_path)
    
    scan_info['proarc_import'] = 'in_folder'
    scan_info['current_dir'] = new_path

    proarc_import_path = os.path.join(project,scan_info['dir_name'])

    device = scan_info.get('device','oldprints/EOD')
    start_import(proarc_import_path,device,user)
