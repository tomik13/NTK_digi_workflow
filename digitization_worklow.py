import os
import json
from datetime import datetime

from OCR import ocr_send, ocr_try_retrieve
from load_scan_dirs import load_scan_dirs
from send_to_proarc import create_periodical_objects
from start_import_scans import start_import_scans
from utils.organize import load_periodicals_info,load_scan_lists,save_periodicals_info,save_scan_lists,load_scan_list,save_scan_list
from archive import archive_scan_folder
from config import data_directory


DOING_OCR = True
DOING_PROARC_OBJECT_PERI = True
DOING_PROARC_OBJCET_MONO = False
DOING_PROARC_IMPORT = True
DOING_ARCHIVING = True
DOING_LIST_FOR_HUMANS = True

scan_import_dir = '/mnt/moon/DIGITALIZACE/WOKRFLOW_TEST/new_scans'
control_list_dir = '/mnt/moon/DIGITALIZACE/WORKFLOW_TEST/lists_scans'

# make a list of new arrivals

def timestamp_now():
    return datetime.now().strftime("%Y%m%d%H%M%S")

timestamp = timestamp_now()

cl = load_scan_dirs()

cls = load_scan_list(data_directory)
periodicals_info = load_periodicals_info(data_directory)

for scan_info in cl:
    scan_info['load_batch'] = f'batch_{timestamp}'
    cls.append(scan_info)

for scan_info in cls:
        # if scan_info.get('problems'):
        #     continue

        if DOING_OCR:
            if not scan_info.get('ocr_state') or scan_info['ocr_state'] == 'ready':
                ocr_send(scan_info)

        # always retrieve done ocrs
        if scan_info.get('ocr_state') == 'sent':
            ocr_try_retrieve(scan_info)


        if scan_info.get('ocr_state') == 'done':
            if DOING_PROARC_OBJECT_PERI:
                if not scan_info.get('proarc_object') and scan_info.get('type') == 'SE':
                    create_periodical_objects(scan_info,periodicals_info)
            if DOING_PROARC_IMPORT:
                if not scan_info.get('proarc_import'):
                    start_import_scans(scan_info)

        if DOING_ARCHIVING:
            if scan_info.get('urn'):
                archive_scan_folder(scan_info)

            
            

save_scan_list(cls,data_folder=data_directory)
save_periodicals_info(data_folder=data_directory,periodicals_info=periodicals_info)