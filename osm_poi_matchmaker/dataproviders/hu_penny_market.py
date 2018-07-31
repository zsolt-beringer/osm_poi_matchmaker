# -*- coding: utf-8 -*-

try:
    import traceback
    import logging
    from osm_poi_matchmaker.libs.address import clean_javascript_variable
    from osm_poi_matchmaker.libs.osm import query_postcode_osm_external
    from osm_poi_matchmaker.libs.poi_dataset import POIDataset
except ImportError as err:
    print('Error {0} import module: {1}'.format(__name__, err))
    traceback.print_exc()
    exit(128)

POI_DATA = ''


class hu_penny_market():

    def __init__(self, session, download_cache, prefer_osm_postcode, filename='hu_penny_market.json'):
        self.session = session
        self.link = POI_DATA
        self.download_cache = download_cache
        self.prefer_osm_postcode = prefer_osm_postcode
        self.filename = filename

    @staticmethod
    def types():
        data = [{'poi_code': 'hupennysup', 'poi_name': 'Penny Market', 'poi_type': 'shop',
                 'poi_tags': "{'shop': 'supermarket', 'operator': 'Penny Market Kft.', 'brand': 'Penny Market', 'addr:country': 'HU', 'internet_access': 'wlan', 'internet_access:fee': 'no', 'internet_access:ssid': 'PENNY FREE WLAN', 'email': 'ugyfelszolgalat@penny.hu', 'facebook': 'https://www.facebook.com/PennyMarketMagyarorszag', 'instagram': 'https://www.instagram.com/pennymarkethu', 'youtube': 'https://www.youtube.com/channel/UCSy0KKUrDxVWkx8qicky_pQ', 'payment:cash': 'yes', 'payment:debit_cards': 'yes', 'ref:vatin:hu': '10969629-2-44'}",
                 'poi_url_base': 'https://www.penny.hu', 'poi_search_name': '(penny market|penny)'}]
        data = POIDataset()
        data.nonstop = None
        data.phone = None
        data.email = None
        data.public_holiday_open = False
        return data

    def process(self):
        logging.warning('Not implemented. Skipping ...')
