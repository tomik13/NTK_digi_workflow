# stuff for rummaging in NDK packages

import sys
import os
import lxml.etree as e

# potrebuju vytahnout uuid, rootuuid, record sysno, model.
# kontrola, yda je uuid v krameriovi
# pokud ano, pak nechci nahravat a chci nakem yalogovat varovani
# kontrola, zda je root v krameriovi
# pokud ne, pak budu chtit pridavat link do aleph a mozna hlaseni
# kontrola, zda ma aleph link do krameria. Pokud ne, pak ho chci pridavat

NDK_mets_ns_dict = {
    'mods'      : 'http://www.loc.gov/mods/v3',
    'mets'      : "http://www.loc.gov/METS/",
    'oai_dc'    : "http://www.openarchives.org/OAI/2.0/oai_dc/",
    'xlink'     : "http://www.w3.org/1999/xlink",
    'dc'        : "http://purl.org/dc/elements/1.1/"
}


def mine_mets(NDK_PSP_dir):
    URNNBN = os.path.basename(NDK_PSP_dir)
    mets_file_name = f"mets_{URNNBN}.xml"
    mets_file_path = f"{NDK_PSP_dir}/{mets_file_name}"
    mets = e.parse(mets_file_path)

    logical_map = mets.xpath("//mets:structMap[@TYPE='LOGICAL']//@DMDID",namespaces = NDK_mets_ns_dict)

    # logical_map = list(map(lambda x : x.split(),logical_map))

    res = {}

    res['root'] = logical_map[0]
    res['tail'] = logical_map[-1]

    # print(logical_map)

    for x in logical_map:
        res[x] = {
            'depth' : int(mets.xpath(f"count(//mets:structMap[@TYPE='LOGICAL']//*[@DMDID = '{x}']/ancestor::mets:div)",namespaces = NDK_mets_ns_dict)),
            'title' : mets.xpath(f"//*[@ID='{x}']//mods:title/text()",namespaces = NDK_mets_ns_dict),
            'uuid' : mets.xpath(f"//*[@ID='{x}']//mods:identifier[@type = 'uuid']/text()",namespaces = NDK_mets_ns_dict),
            'rec_sysno' : mets.xpath(f"//*[@ID='{x}']//mods:recordIdentifier/text()",namespaces = NDK_mets_ns_dict),
            'number' : mets.xpath(f"//*[@ID='{x}']//mods:partNumber/text()",namespaces = NDK_mets_ns_dict),
            'date' : mets.xpath(f"//*[@ID='{x}']//mods:dateIssued/text()",namespaces = NDK_mets_ns_dict),
            'sig' : mets.xpath(f"//*[@ID='{x}']//mods:shelfLocator/text()",namespaces = NDK_mets_ns_dict),
            'model' : mets.xpath(f"//*[@ID='DCMD{x[x.index('_'):]}']//dc:type/text()",namespaces=NDK_mets_ns_dict)
        }

    return res


if __name__=='__main__':
    x = mine_mets('/mnt/home/digi_workflow/testdata/NDK_mets/to_import/aba013-00041j')

    print(*[f"{k} {x[k]}" for k in x], sep='\n')