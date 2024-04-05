import os

def archive_NDK(digi_info):
    urnnbnb = digi_info['urnnbn']
    archive_dir = x if (x := digi_info.get('archive_dir')) else '/mnt/moon/DIGITALIZACE/WORKFLOW_TEST/to_archive'
    archive_path = os.path.join(archive_dir,urnnbnb)
    current_dir = digi_info['current_dir']
    if not os.path.exists(archive_dir):
        os.mkdir(archive_dir)
    os.rename(current_dir,archive_path)
    digi_info['current_dir']=archive_path
    digi_info['archived'] = True


def archive_scan_folder(scan_info):
    dir_name = scan_info['dir_name']
    archive_dir = x if (x := scan_info.get('scan_archive')) else '/mnt/moon/DIGITALIZACE/WORKFLOW_TEST/scans_to_archive'
    archive_path = os.path.join(archive_dir,dir_name)
    current_dir = scan_info['current_dir']
    if not os.path.exists(archive_dir):
        os.mkdir(archive_dir)
    os.rename(current_dir,archive_path)
    scan_info['current_dir']=archive_path
    scan_info['archived'] = True