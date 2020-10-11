# -*- coding: utf-8 -*-

try:
    import traceback
    import logging
    import sys
    import os
    import json
    from osm_poi_matchmaker.libs.soup import save_downloaded_soup
    from osm_poi_matchmaker.libs.address import extract_street_housenumber_better_2, clean_city, clean_phone_to_str
    from osm_poi_matchmaker.libs.geo import check_hu_boundary
    from osm_poi_matchmaker.libs.osm_tag_sets import POS_HU_GEN, PAY_CASH
    from osm_poi_matchmaker.utils.data_provider import DataProvider
    from osm_poi_matchmaker.utils.enums import FileType
except ImportError as err:
    logging.error('Error {error} import module: {module}', module=__name__, error=err)
    logging.error(traceback.print_exc())
    sys.exit(128)


class hu_yves_rocher(DataProvider):

    def constains(self):
        self.link = 'https://storelocator.yves-rocher.eu/api/v1/map/stores'
        self.POI_COMMON_TAGS = "'shop': 'cosmetics', 'operator': 'Yves Rocher Hungary Kft. '," \
                               "'brand': 'Yves Rocher', 'brand:wikidata': 'Q28496595', " \
                               "'brand:wikipedia': 'en:Yves Rocher (company)', " \
                               "'contact:email': 'vevoszolgalat@yrnet.com', " \
                               "'contact:facebook': 'https://www.facebook.com/YvesRocherHungary/', " \
                               "'contact:youtube': 'https://www.youtube.com/channel/UC6GA7lucPWgbNlC_MoomB9g', " \
                               "'contact:instagram': 'https://www.instagram.com/yves_rocher_magyarorszag/', " \
                               "'operator:addr': '1132 Budapest, Váci út 20-26.', 'ref:vatin': 'HU10618646', " \
                               "'ref:vatin:hu': '10618646-2-41', 'ref:HU:company': '01-09-079930', "
        self.filetype = FileType.json
        self.filename = '{}.{}'.format(self.__class__.__name__, self.filetype.name)

    def types(self):
        self.__types = [{'poi_code': 'huyvesrcos', 'poi_name': 'Yves Rocher', 'poi_type': 'cosmetics',
                 'poi_tags': "{" + self.POI_COMMON_TAGS + POS_HU_GEN + PAY_CASH + "'air_conditioning': 'yes'}",
                 'poi_url_base': 'https://www.yves-rocher.hu/', 'poi_search_name': 'yves rocher',
                         'osm_search_distance_perfect': 2000, 'osm_search_distance_safe': 200,
                         'osm_search_distance_unsafe': 15}]
        return self.__types

    def process(self):
        try:
            soup = save_downloaded_soup('{}'.format(self.link), os.path.join(self.download_cache, self.filename),
                                        self.filetype)
            if soup is not None:
                text = json.loads(str(soup))
                for poi_data in text.get('list'):
                    try:
                        if poi_data.get('country_id') != 3:
                            continue
                        else:
                            self.data.name = 'Yves Rocher'
                            self.data.code = 'huyvesrcos'
                            self.data.lat, self.data.lon = \
                                check_hu_boundary(poi_data.get('latitude'), poi_data.get('longitude'))
                            self.data.website = 'https://www.yves-rocher.hu{}/'.format(poi_data.get('request_path'))
                            opening = poi_data.get('hours')
                            for i in range(0, 7):
                                if i in opening:
                                    self.data.day_open(i, opening[i]['hour_from'])
                                    self.data.day_close(i, opening[i]['hour_to'])
                            self.data.postcode = poi_data.get('zip')
                            self.data.street, self.data.housenumber, self.data.conscriptionnumber = \
                                extract_street_housenumber_better_2(poi_data.get('address'))
                            self.data.city = clean_city(poi_data.get('city'))
                            self.data.original = poi_data.get('address')
                            if poi_data.get('phone') is not None and poi_data.get('phone') != '':
                                self.data.phone = clean_phone_to_str(poi_data.get('phone'))
                            if poi_data.get('mobile') is not None and poi_data.get('mobile') != '' \
                                    and self.data.phone is not None:
                                self.data.phone = '{};{}'.format(self.data.phone, clean_phone_to_str(poi_data.get('mobile')))
                            elif poi_data.get('mobile') is not None and poi_data.get('mobile') != '' \
                                    and self.data.phone is None:
                                self.data.phone = clean_phone_to_str(poi_data.get('mobile'))
                            self.data.public_holiday_open = False
                            self.data.add()
                    except Exception as e:
                        logging.error(e)
                        logging.error(poi_data)
                        logging.error(traceback.print_exc())
        except Exception as e:
            logging.error(e)
            logging.error(traceback.print_exc())
