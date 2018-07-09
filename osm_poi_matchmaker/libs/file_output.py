# -*- coding: utf-8 -*-

try:
    import math
    import logging
    import os
    import datetime
except ImportError as err:
    print('Error {0} import module: {1}'.format(__name__, err))
    exit(128)

POI_TAGS = {'poi_name': 'name', 'poi_city': 'addr:city', 'poi_postcode': 'addr:postcode',
            'poi_addr_street': 'addr:street', 'poi_addr_housenumber': 'addr:housenumber',
            'poi_conscriptionnumber': 'addr:conscriptionnumber', 'poi_branch': 'branch', 'poi_email': 'email',
            'poi_opening_hours': 'opening_hours'}


def ascii_numcoder(text):
    output = ''
    for i in text:
        if i in range(0, 10, 1):
            output += i
        else:
            output += str(ord(i))
    return output


def save_csv_file(path, file, data, message):
    # Save file to CSV file
    logging.info('Saving {0} to file: {1}'.format(message, file))
    res = data.to_csv(os.path.join(path, file))
    logging.info('The {0} was sucessfully saved'.format(file))


def generate_osm_xml(df):
    from lxml import etree
    import lxml
    osm_xml_data = etree.Element('osm', version='0.6', generator='JOSM')
    id = -1
    current_id = id
    for index, row in df.iterrows():
        current_id = id if row['osm_id'] is None else row['osm_id']
        osm_timestamp = '' if row['osm_timestamp'] is None else row['osm_timestamp']
        osm_changeset = '99999' if row['osm_changeset'] is None else row['osm_changeset'] + 1
        osm_version = '99999' if row['osm_version'] is None else row['osm_version']
        if row['node'] is None or (row['node'] == True or math.isnan(row['node'])):
            main_data = etree.SubElement(osm_xml_data, 'node', action='modify', id=str(current_id),
                                         lat='{}'.format(row['poi_lat']), lon='{}'.format(row['poi_lon']),
                                         user='{}'.format('KAMI'), timestamp='{}'.format(osm_timestamp),
                                         uid='{}'.format('4579407'), changeset='{}'.format(osm_changeset),
                                         version='{}'.format(osm_version))
            if current_id > 0:
                comment = etree.Comment(' OSM link: https://osm.org/node/{} '.format(str(current_id)))
                osm_xml_data.append(comment)
        elif row['node'] is not None and row['node'] == False:
            main_data = etree.SubElement(osm_xml_data, 'way', action='modify', id=str(current_id),
                                         user='{}'.format('KAMI'), timestamp='{}'.format(osm_timestamp),
                                         uid='{}'.format('4579407'), changeset='{}'.format(osm_changeset),
                                         version='{}'.format(osm_version))
            # Add way nodes without any modification)
            try:
                for n in row['osm_nodes']:
                    data = etree.SubElement(main_data, 'nd', ref=str(n))
            except TypeError as err:
                logging.warning('Missing nodes on this way: {}.'.format(row['osm_id']))
            # Add node reference as comment for existing POI
            if current_id > 0:
                comment = etree.Comment(' OSM link: https://osm.org/way/{} '.format(str(current_id)))
                osm_xml_data.append(comment)
        # Add original POI coordinates as comment
        comment = etree.Comment(' Original coordinates: {} '.format(row['poi_geom']))
        osm_xml_data.append(comment)
        # Add original POI tags as comment
        if row['osm_live_tags'] is not None:
            for k, v in row['osm_live_tags'].items():
                # do something with value
                if isinstance(v, str):
                    row['osm_live_tags'][k] = v.replace('--', '\-\-').replace('\n', '')
        comment = etree.Comment(' Original tags: {} '.format(row['osm_live_tags']))
        osm_xml_data.append(comment)
        # Using already definied OSM tags if exists
        if row['osm_live_tags'] is not None:
            tags = row['osm_live_tags']
        else:
            tags = {}
        # Adding POI common tags
        if row['poi_tags'] is not None:
            tags.update(eval(row['poi_tags']))
        # Overwriting with data from data providers
        for k, v in POI_TAGS.items():
            if row[k] is not None:
                tags[v] = row[k]
        if row['poi_phone'] is not None and not math.isnan(row['poi_phone']):
            tags['phone'] = '+{:d}'.format(int(row['poi_phone']))
        if row['poi_url_base'] is not None and row['poi_website'] is not None:
            tags['website'] = '{}{}'.format(row['poi_url_base'], row['poi_website'])
        elif row['poi_url_base'] is not None:
            tags['website'] = row['poi_url_base']
        tags['source'] = 'website'
        tags['source:date'] = '{:{dfmt}}'.format(datetime.datetime.now(), dfmt='%Y-%m-%d')
        tags['import'] = 'osm_poi_matchmaker'
        # Rendering tags to the XML file
        for k, v in tags.items():
            xml_tags = etree.SubElement(main_data, 'tag', k=k, v='{}'.format(v))
        osm_xml_data.append(main_data)
        id -= 1
    return lxml.etree.tostring(osm_xml_data, pretty_print=True, xml_declaration=True, encoding="UTF-8")
