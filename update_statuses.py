import requests as r
import lxml.etree as e
from utils.kramerius import check_upload_process_state,check_uuid_inK5

nss = {
    'marc':'http://www.loc.gov/MARC21/slim'
}



def update_kramerius_status(digi_info):
        itemuuid = digi_info['item']
        if (k5status := check_uuid_inK5(itemuuid)) == 404:
            digi_info['kramerius'] = False
        elif k5status == 200:
            digi_info['kramerius'] = True
        else:
            raise Exception('some bs with checking kramerius state')

def update_kramerius_upload_process_status(digi_info):
    process_uuid = digi_info.get('upload_uuid')
    if not process_uuid: 
        digi_info['upload_state'] = 'not_started'
        return
    state, batch_state = check_upload_process_state(process_uuid)
        
    print(state, batch_state)
    if state == "FINISHED":
        digi_info['upload_state'] = batch_state
    else:
        digi_info['upload_state'] = state

    if digi_info['upload_state'] == 'BATCH_FINISHED':
        digi_info['kramerius'] = True

def update_aleph_link(rec):
    url = f'http://aleph.techlib.cz/OAI?verb=GetRecord&metadataPrefix=marc21&Identifier=oai:aleph.techlib.cz:STK01-{rec["sysno"]}'
    res = r.get(url)
    ne = e.XML(res.content)

    link = ne.xpath('//marc:datafield[@tag=856 and @ind1=4 and @ind2=1]/*[@code = "u"]/text()', namespaces=nss)
    links = [f for f in link if 'kramerius.techlib' in f]
    print(f"{rec['sysno']} : {links}")
    print([f for f in link if rec['root'] in  f])
    rec['aleph'] = bool(links)
