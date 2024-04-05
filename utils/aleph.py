# stuff for harvesting data from the aleph catalog

import json
import datetime
import requests as r
import lxml.etree as e


LINK_PREFIX="https://kramerius.techlib.cz/kramerius-web-client/uuid/uuid:"
aleph_import_template="{sysno} 85641 L $$u{link}$$yDigitalizovaný dokument"


def generate_aleph_line(rec):
    if rec['kramerius'] and not rec['aleph']:
        return aleph_import_template.format(sysno=rec['sysno'],link = f"{LINK_PREFIX}{rec['root']}")
    else:
        return
    
nss = {
    'marc':'http://www.loc.gov/MARC21/slim'
}


import lxml.etree as e
import requests as r
import xmltodict as xd


oai_url_base = f'http://aleph.techlib.cz/OAI?verb=GetRecord&metadataPrefix=marc21&Identifier=oai:aleph.techlib.cz:STK01-'

clean_template = e.parse('utils/oai_marc_clean.xsl')
clean = e.XSLT(clean_template)

def aleph_oai_marcSLIM(SYSNO):
    url = oai_url_base+SYSNO
    res = r.get(url)
    if res.status_code != 200:
        return res.status_code
    else:
        ne = e.XML(res.content)
        nne = clean(ne)
        return nne

def aleph_dict_ids(SYSNO):
    small_template = e.parse('utils/cnb_di.xsl')
    small = e.XSLT(small_template)
    ne = aleph_oai_marcSLIM(SYSNO)
    nne = small(ne)
    d = xd.parse(str(nne))
    return d['collection']['record']


if __name__ == '__main__':
    pass    



        