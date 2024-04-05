from utils.aleph import aleph_oai_marcSLIM
import lxml.etree as e

stylesheet = e.parse('utils/rd_export_tl.xsl')
transform = e.XSLT(stylesheet)

def make_RD_record(digi_info):
    recId = digi_info['001'] if '001' in digi_info else digi_info['sysno']
    ne = aleph_oai_marcSLIM(digi_info['sysno'])
    nr = transform(ne,FMT=f"'{digi_info['FMT']}'",recId = recId)
    return nr

def make_RD_collection(control_list,filename):
    newBatch = e.parse('hlaseniRD/empty.xml')
    root = newBatch.getroot()
    for urn in control_list:
        digi_info = control_list[urn]
        nr = make_RD_record(digi_info)
        root.append(nr.getroot())
        digi_info['RD_batch_file'] = filename
    newBatch.write(filename, encoding='utf-8', xml_declaration=True, pretty_print=True)

    

