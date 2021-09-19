import json

import SkinXML


def test_skin_xml_vars():
    root = SkinXML.load('Odyssey')
    xml_variables = root.find('variables')

    rv = {}
    for ss in xml_variables:
        if ss.tag == 'variablegroup':
            xml_var = ss.find('variable')
        else:
            xml_var = ss
        name = xml_var.find('name')
        default = xml_var.find('default')
        # print(name.text, default.text)
        if default is not None and default.text is not None \
                and len(str(default.text)) > 0:
            rv[name.text] = str(default.text)
    print(rv)


def test_skin_xml():
    xml = SkinXML.load('skin-bookclub-custom')
    cover = xml.find('default')
    cover = cover.find('cover').text
    # cover = xml[0][0]
    # cover = xml.findtext('showListOnArchive')
    # print(cover)
    cover_group = json.loads(cover)
    # print(cover_group)
    for cover in cover_group:
        if cover['name'] == 'cover-thumbnail-1':
            for cover_item in cover['data']:
                print(cover_item['title'])
