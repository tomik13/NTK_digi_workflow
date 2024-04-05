import json
import os
from utils.kramerius import import_package_own_process

def start_upload_packages(control_list):
    for urn in control_list:
        digi_info = control_list[urn]

        if not digi_info['kramerius']:
            import_package_own_process(digi_info)




if __name__=="__main__":
    control_list_dir = "testfiles"
    cl_list = [l for l in os.listdir(control_list_dir)]

    print(cl_list)

    cls = {}

    for cl in cl_list:
        print(f'working on list {cl}')
        control_list_path = os.path.join(control_list_dir,cl)
        with open(control_list_path,'rt') as f:
            cls[cl] = json.load(f)

        list=cls[cl]
        for urn in list:
            digi_info = list[urn]

            if not digi_info['kramerius']:
                import_package_own_process(digi_info)

        with open(control_list_path,'wt') as f:
            json.dump(list,f)
