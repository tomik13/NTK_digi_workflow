from utils.proarc import make_year,make_issue


def create_periodical_objects(scan_info, periodicals_info):
    if not scan_info.get('type') == 'SE':
        return
    
    if not periodicals_info.get(scan_info['sysno']):
        scan_info['problems'].append('Periodical without root object')
        return
    
    title_info = periodicals_info[scan_info['sysno']]
    root_uuid = title_info['root_uuid']

    show_year = '-'.join(map(lambda x: str(int(x)), scan_info['year'].split('_')))
    show_volume = str(int(scan_info['volume']))
    show_issue = ','.join(map(lambda x: str(int(x)), scan_info['issue'].split('_')))


    if not scan_info['volume'] in title_info:
        volume_uuid = make_year(root_uuid,show_year,show_volume)
        title_info[scan_info['volume']] = volume_uuid
    else:
        volume_uuid = title_info[scan_info['volume']]
    issue_uuid = make_issue(volume_uuid, show_year,show_issue)

    scan_info['proarc_object'] = 'auto'
    scan_info['proarc_uuid'] = issue_uuid