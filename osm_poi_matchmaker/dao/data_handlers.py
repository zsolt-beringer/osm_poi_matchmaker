# -*- coding: utf-8 -*-

try:
    import traceback
    import hashlib
    import logging
    from osm_poi_matchmaker.dao.data_structure import City, POI_common, POI_address
    from osm_poi_matchmaker.libs import address
except ImportError as err:
    print('Error {0} import module: {1}'.format(__name__, err))
    traceback.print_exc()
    exit(128)

POI_COLS = ['poi_code', 'poi_postcode', 'poi_city', 'poi_name', 'poi_branch', 'poi_website', 'original',
            'poi_addr_street',
            'poi_addr_housenumber', 'poi_conscriptionnumber', 'poi_ref', 'poi_geom']


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        try:
            instance = model(**kwargs)
            session.add(instance)
            return instance
        except Exception as e:
            traceback.print_exc()
            raise (e)


def insert_city_dataframe(session, city_df):
    city_df.columns = ['city_post_code', 'city_name']
    try:
        for index, city_data in city_df.iterrows():
            get_or_create(session, City, city_post_code=city_data['city_post_code'],
                          city_name=address.clean_city(city_data['city_name']))
    except Exception as e:
        logging.error(city_data)
        session.rollback()
        print(e)
    else:
        session.commit()


def insert_common_dataframe(session, common_df):
    common_df.columns = ['poi_name', 'poi_tags', 'poi_url_base', 'poi_code']
    try:
        for index, poi_common_data in common_df.iterrows():
            get_or_create(session, POI_common, **poi_common_data)
    except Exception as e:
        session.rollback()
        print(e)
    else:
        session.commit()


def search_for_postcode(session, city_name):
    city_col = session.query(City.city_post_code).filter(City.city_name == city_name).all()
    if len(city_col) == 1:
        return city_col
    else:
        logging.info('Cannot determine the post code from city name ({}).'.format(city_name))
        return None


def insert_poi_dataframe(session, poi_df):
    poi_df.columns = POI_COLS
    poi_df[['poi_postcode']] = poi_df[['poi_postcode']].fillna('0000')
    poi_df[['poi_postcode']] = poi_df[['poi_postcode']].astype(int)
    poi_dict = poi_df.to_dict('records')
    try:
        for poi_data in poi_dict:
            city_col = session.query(City.city_id).filter(City.city_name == poi_data['poi_city']).filter(
                City.city_post_code == poi_data['poi_postcode']).first()
            common_col = session.query(POI_common.pc_id).filter(POI_common.poi_code == poi_data['poi_code']).first()
            poi_data['poi_addr_city'] = city_col
            poi_data['poi_common_id'] = common_col
            if 'poi_name' in poi_data: del poi_data['poi_name']
            if 'poi_code' in poi_data: del poi_data['poi_code']
            get_or_create(session, POI_address, **poi_data)
    except Exception as e:
        session.rollback()
        print(e)
    else:
        logging.info('Successfully added the dataset.')
        session.commit()


def insert_type(session, type_data):
    try:
        for i in type_data:
            get_or_create(session, POI_common, **i)
    except Exception as e:
        session.rollback()
        print(e)
    else:
        logging.info('Successfully added the dataset.')
        session.commit()


def insert(session, **kwargs):
    try:
        city_col = session.query(City.city_id).filter(City.city_name == kwargs['poi_city']).filter(
            City.city_post_code == kwargs['poi_postcode']).first()
        common_col = session.query(POI_common.pc_id).filter(POI_common.poi_code == kwargs['poi_code']).first()
        kwargs['poi_addr_city'] = city_col
        kwargs['poi_common_id'] = common_col
        kwargs['poi_hash'] = hashlib.sha512(
            '{}{}{}{}{}{}'.format(kwargs['poi_code'], kwargs['poi_postcode'], kwargs['poi_city'],
                                  kwargs['poi_addr_street'], kwargs['poi_addr_housenumber'],
                                  kwargs['poi_conscriptionnumber']).lower().replace(' ', '').encode(
                'utf-8')).hexdigest()
        if 'poi_name' in kwargs: del kwargs['poi_name']
        if 'poi_code' in kwargs: del kwargs['poi_code']
        get_or_create(session, POI_address, **kwargs)
        session.commit()
    except Exception as e:
        print(e)
    finally:
        session.close()
