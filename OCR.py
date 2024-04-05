import os


base_ocr_directory = '/mnt/moon/DIGITALIZACE/EDITOR/ocr/'
ocr_result_directory = os.path.join(base_ocr_directory,'done')
ocr_lang_dirs = {lan : os.path.join(base_ocr_directory,lan) for lan in ['eng','ces','deu'] }

def ocr_send(scan_info):
    lan = ln if (ln := scan_info.get('ocr_lan')) else 'ces'
    ocr_path = os.path.join(ocr_lang_dirs[lan],scan_info['dir_name'])
    presumed_done_path = os.path.join(ocr_result_directory,scan_info['dir_name'])
    scan_info['ocr_result'] = presumed_done_path
    scan_info['ocr_return'] = scan_info['current_dir']
    os.replace(scan_info['current_dir'],ocr_path)
    scan_info['current_dir'] = ocr_path
    scan_info['ocr_state'] = 'sent'

def ocr_try_retrieve(scan_info):
    if os.path.exists(scan_info['ocr_result']):
        os.replace(scan_info['ocr_result'],scan_info['ocr_return'])
        scan_info['current_dir'] = scan_info['ocr_return']
        scan_info['ocr_state'] = 'done'