# -*- coding: utf-8 -*-

try:
    import traceback
    import logging
    import os
    import re
    import json
    import pandas as pd
    from osm_poi_matchmaker.dao.data_handlers import insert_poi_dataframe
    from osm_poi_matchmaker.libs.soup import save_downloaded_soup
    from osm_poi_matchmaker.libs.address import extract_street_housenumber_better, clean_city, clean_javascript_variable
    from osm_poi_matchmaker.libs.geo import check_geom
except ImportError as err:
    print('Error {0} import module: {1}'.format(__name__, err))
    traceback.print_exc()
    exit(128)

POI_COLS = ['poi_code', 'poi_postcode', 'poi_city', 'poi_name', 'poi_branch', 'poi_website', 'original',
            'poi_addr_street',
            'poi_addr_housenumber', 'poi_conscriptionnumber', 'poi_ref', 'poi_geom']


class hu_benu():

    def __init__(self, session, link, download_cache, filename='hu_benu.json'):
        self.session = session
        self.link = link
        self.download_cache = download_cache
        self.filename = filename

    def types(self):
        data = [{'poi_code': 'hubenupha', 'poi_name': 'Benu gyógyszertár',
                 'poi_tags': "{'amenity': 'pharmacy', 'dispensing': 'yes', 'payment:cash': 'yes', 'payment:debit_cards': 'yes'}", 'poi_url_base': 'https://www.benu.hu'}]
        return data

    def process(self):
        soup = save_downloaded_soup('{}'.format(self.link), os.path.join(self.download_cache, self.filename))
        insert_data = []
        if soup != None:
            text = json.loads(soup.get_text())
            for poi_data in text:
                street, housenumber, conscriptionnumber = extract_street_housenumber_better(
                    poi_data['street'])
                if 'BENU Gyógyszertár' not in poi_data['title']:
                    name = poi_data['title'].strip()
                    branch = None
                else:
                    name = 'Benu gyógyszertár'
                    branch = poi_data['title'].strip()
                code = 'hubenupha'
                website = poi_data['description'].strip() if poi_data['description'] is not None else None
                city = clean_city(poi_data['city'])
                postcode = poi_data['postal_code'].strip()
                geom = check_geom(poi_data['lat'], poi_data['lng'])
                original = poi_data['street']
                ref = None
                insert_data.append(
                    [code, postcode, city, name, branch, website, original, street, housenumber, conscriptionnumber,
                     ref, geom])
            if len(insert_data) < 1:
                logging.warning('Resultset is empty. Skipping ...')
            else:
                df = pd.DataFrame(insert_data)
                df.columns = POI_COLS
                insert_poi_dataframe(self.session, df)
