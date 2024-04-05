import os
import json

from load_packages import load_packages
from update_statuses import update_kramerius_status,update_kramerius_upload_process_status,update_aleph_link
from utils.kramerius import import_package_own_process,clear_import_stages
from utils.aleph import generate_aleph_line
from archive import archive_NDK
from make_RD_record import make_RD_collection
from utils.organize import load_scan_lists,save_scan_list,load_export_list,load_scan_list,load_periodicals_info,save_export_list
from config import aleph_lines_directory,data_directory

from datetime import datetime

# what are we doing? We always update statuses and archive uploaded stuff.

DOING_UPLOADS = False
DOING_ALEPH = False
REDOING_ALEPH = False
DOING_RD = True



sysnos_to_upload = []
urns_to_upload = []
uuids_to_upload = []


def timestamp_now():
    return str(int(datetime.now().strftime("%Y%m%d_%H%M%S")))

timestamp = timestamp_now()

def RD_filename(fin):
    return f"aba013_h{'_'+fin if fin else ''}_{timestamp}"

aleph_lines_file_name = f'digi_kram_856_{timestamp}'


# load latest additions
pkgs = load_packages()

# load all lists to go through and take care of

cl_list = load_export_list(data_directory)

for urn in pkgs:
    cl_list[urn] = pkgs[urn]
    cl_list[urn]['load_batch'] = f"batch_{timestamp}"


scan_list = load_scan_list(data_directory)

scans_dict = {}
for scan_info in scan_list:
    if 'NTK_digi_id' in scan_info:
        scans_dict[scan_info['NTK_digi_id']] = scan_info

aleph_lines = []
RD_h = {}

# push along all packages in all lists

for urn in cl_list:
        digi_info = cl_list[urn]

        # try to identify which scans this object comes from
        if 'NTK_digi_id' in digi_info:
            scan_info = scans_dict.get(digi_info['NTK_digi_id'])
            print(digi_info)
            if scan_info:
                digi_info['fin'] = scan_info['fin']
                digi_info['archive_dir'] = scan_info['NDK_archive']
                scan_info['urn'] = urn

        # update states (unless explicitely pointless)
        if not digi_info['kramerius']:
            update_kramerius_upload_process_status(digi_info)
        update_aleph_link(digi_info)



        # see what stage it is and move it along

        if DOING_UPLOADS:
            # if it's not in the library, check if its uploading. If it is not, start the upload
            # if it has delayed upload, dont upload it yet
            if not digi_info['kramerius']:
                update_kramerius_upload_process_status(digi_info)
                if digi_info['sysno'] in sysnos_to_upload or digi_info['urnnbn'] in urns_to_upload or digi_info['item'] in uuids_to_upload:
                    if digi_info['upload_state'] == 'not_started':
                        if not (date := digi_info.get('scheduled_upload')) or date <= timestamp:
                            import_package_own_process(digi_info)
                    else:
                        print(f'{digi_info} is online')

            # if it is already uploaded, archive the package
                
        if digi_info['kramerius']:
            if not digi_info.get('archived'):
                archive_NDK(digi_info)

        
        if DOING_ALEPH:
            if digi_info['kramerius'] and not digi_info['aleph']:
                if not digi_info.get('aleph_batch') or REDOING_ALEPH:
                    new_line = generate_aleph_line(digi_info)
                    if not new_line in aleph_lines:
                        aleph_lines.append(new_line)
                    digi_info['aleph_batch'] = aleph_lines_file_name

        if DOING_RD:
            if digi_info['aleph'] and not digi_info.get('RD_h_batch'):
                print(f'I think we should send this one up to RD. FMT : {digi_info["FMT"]}')
                if digi_info["FMT"] != 'SE':
                    fin = digi_info.get('fin', '')
                    if not fin in RD_h:
                        RD_h[fin] = []
                    RD_h[fin].append(digi_info)
                    digi_info['RD_h_batch'] = RD_filename(fin)



for fin in RD_h:
    RD_list = RD_h[fin]
    filename = RD_filename(fin)
    make_RD_collection(RD_list,filename)


clear_import_stages()

save_export_list(cl_list,data_directory)

save_scan_list(scan_list,data_folder=data_directory)

aleph_lines_file_path = os.path.join(aleph_lines_directory,aleph_lines_file_name)
if aleph_lines:
    with open(aleph_lines_file_path,'wt') as f:
        f.writelines(list(map(lambda x : x + '\n', aleph_lines)))