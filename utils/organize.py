import json
import os



scan_import_dir = '/mnt/moon/DIGITALIZACE/WOKRFLOW_TEST/new_scans'
control_list_dir = '/mnt/moon/DIGITALIZACE/WORKFLOW_TEST/lists_scans'

def save_scan_lists(cls):
    for cl in cls:
        with open(os.path.join(control_list_dir,cl),'wt') as f:
            json.dump(cls[cl],f, indent=4)

def save_scan_list(scan_list,data_folder):
    with open(os.path.join(data_folder,'list_scan_folders'),'wt') as f:
        json.dump(scan_list,f, indent=4)

def save_periodicals_info(data_folder,periodicals_info):
    with open(os.path.join(data_folder,'periodicals_info'),'wt') as f:
        json.dump(periodicals_info,f, indent=4)
 
def load_scan_lists(control_list_dir):
    cls = {}
    cl_list = os.listdir(control_list_dir)
    for cl in cl_list:
        if 'batch' in cl:
            with open(os.path.join(control_list_dir,cl),'rt') as f:
                cls[cl] = json.load(f)

    return cls

def load_scan_list(data_folder):
    with open(os.path.join(data_folder,'list_scan_folders'),'rt') as f:
        cl = json.load(f)

    return cl


def load_periodicals_info(data_folder):
    with open(os.path.join(data_folder,'periodicals_info'),'rt') as f:
        periodicals_info = json.load(f)

    return periodicals_info

def load_export_lists(control_list_dir):
    cl_list = os.listdir(control_list_dir)
    cls = {}
    for cl in cl_list:
        with open(os.path.join(control_list_dir,cl),'rt') as f:
            cls[cl] = json.load(f)

    return cls

def load_export_list(data_folder):
    with open(os.path.join(data_folder,'list_urns'),'rt') as f:
        cl = json.load(f)
    return cl


def save_export_lists(cls):
    for cl in cls:
        with open(os.path.join(control_list_dir,cl),'wt') as f:
            json.dump(cls[cl],f, indent=4)

def save_export_list(export_list,data_folder):
   with open(os.path.join(data_folder,'list_urns'),'wt') as f:
        json.dump(export_list,f, indent=4)
