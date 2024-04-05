import os
from utils.aleph import generate_aleph_line
from update_statuses import update_kramerius_status, update_aleph_link
import json

control_list_dir = "testfiles"
cl_list = [l for l in os.listdir(control_list_dir)]

print(cl_list)



cls = {}

def generate_aleph_lines(control_list, filename):
    aleph_lines=[]
    for urn in control_list:
        digi_info = control_list[urn]
        update_kramerius_status(digi_info)
        update_aleph_link(digi_info)
        aleph_lines.append(generate_aleph_line(digi_info))
        digi_info['aleph_import_file'] = filename
    with open(filename,'wt',encoding='utf-8') as f:
        f.writelines(aleph_lines)


for cl in cl_list:
    print(f'working on list {cl}')
    control_list_path = os.path.join(control_list_dir,cl)
    with open(control_list_path,'rt') as f:
        cls[cl] = json.load(f)

    list=cls[cl]
    for urn in list:
        digi_info = list[urn]
        update_kramerius_status(digi_info)
        update_aleph_link(digi_info)
        print(generate_aleph_line(digi_info))

    with open(control_list_path,'wt') as f:
        json.dump(list,f, indent=4)


