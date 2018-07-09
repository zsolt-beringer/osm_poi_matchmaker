# -*- coding: utf-8 -*-
__author__ = 'kami911'

try:
    import traceback
    import numpy as np
    import pandas as pd
    from osm_poi_matchmaker.utils.enums import WeekDaysShort, OpenClose, WeekDaysLongHU
    from osm_poi_matchmaker.libs.opening_hours import OpeningHours
    from osm_poi_matchmaker.libs.geo import check_geom
    from osm_poi_matchmaker.dao import poi_array_structure
except ImportError as err:
    print('Error {0} import module: {1}'.format(__name__, err))
    traceback.print_exc()
    exit(128)

__program__ = 'poi_dataset'
__version__ = '0.0.1'

POI_COLS = poi_array_structure.POI_COLS


class POIDataset:

    def __init__(self):
        self.insert_data = []
        self.clear_all()

    def clear_all(self):
        self.__code = None
        self.__postcode = None
        self.__city = None
        self.__name = None
        self.__branch = None
        self.__website = None
        self.__original = None
        self.__street = None
        self.__housenumber = None
        self.__conscriptionnumber = None
        self.__ref = None
        self.__phone = None
        self.__email = None
        self.__geom = None
        self.__lat = None
        self.__long = None
        self.__nonstop = None
        self.__oh = pd.DataFrame(index=WeekDaysShort, columns=OpenClose)
        self.__lunch_break = {'start': None, 'stop': None}
        self.__opening_hours = None

    @property
    def code(self):
        return (self.__code)

    @code.setter
    def code(self, data):
        self.__code = data

    @property
    def postcode(self):
        return (self.__postcode)

    @postcode.setter
    def postcode(self, data):
        self.__postcode = data

    @property
    def city(self):
        return (self.__city)

    @city.setter
    def city(self, data):
        self.__city = data

    @property
    def name(self):
        return (self.__name)

    @name.setter
    def name(self, data):
        self.__name = data

    @property
    def branch(self):
        return (self.__branch)

    @branch.setter
    def branch(self, data):
        self.__branch = data

    @property
    def website(self):
        return (self.__website)

    @website.setter
    def website(self, data):
        self.__website = data

    @property
    def original(self):
        return (self.__original)

    @original.setter
    def original(self, data):
        self.__original = data

    @property
    def street(self):
        return (self.__original)

    @street.setter
    def street(self, data):
        self.__street = data

    @property
    def housenumber(self):
        return (self.__original)

    @housenumber.setter
    def housenumber(self, data):
        self.__housenumber = data

    @property
    def conscriptionnumber(self):
        return (self.__original)

    @conscriptionnumber.setter
    def conscriptionnumber(self, data):
        self.__conscriptionnumber = data

    @property
    def ref(self):
        return (self.__original)

    @ref.setter
    def ref(self, data):
        self.__ref = data

    @property
    def phone(self):
        return (self.__original)

    @phone.setter
    def phone(self, data):
        self.__phone = data

    @property
    def email(self):
        return (self.__original)

    @email.setter
    def email(self, data):
        self.__email = data

    @property
    def geom(self):
        return (self.__original)

    @geom.setter
    def geom(self, data):
        self.__geom = data

    @property
    def lat(self):
        return self.__lat

    @lat.setter
    def lat(self, lat):
        self.__lat = lat

    @property
    def long(self):
        return self.__long

    @long.setter
    def long(self, long):
        self.__long = long

    def process_geom(self):
        self.geom = check_geom(self.__lat, self.__long)

    @property
    def opening_hours_table(self):
        return (self.__oh)

    @opening_hours_table.setter
    def opening_hours_table(self, data):
       self.__oh = pd.DataFrame(data, index=WeekDaysShort, columns=OpenClose)

    @property
    def nonstop(self):
        return (self.__nonstop)

    @nonstop.setter
    def nonstop(self, data):
        self.__nonstop = data

    @property
    def mo_o(self):
        return (self.__oh.at[WeekDaysShort.mo, OpenClose.open])

    @mo_o.setter
    def mo_o(self, data):
        self.__oh.at[WeekDaysShort.mo, OpenClose.open] = data

    @property
    def tu_o(self):
        return (self.__oh.at[WeekDaysShort.tu, OpenClose.open])

    @tu_o.setter
    def tu_o(self, data):
        self.__oh.at[WeekDaysShort.tu, OpenClose.open] = data

    @property
    def we_o(self):
        return (self.__oh.at[WeekDaysShort.we, OpenClose.open])

    @we_o.setter
    def we_o(self, data):
        self.__oh.at[WeekDaysShort.we, OpenClose.open] = data

    @property
    def th_o(self):
        return (self.__oh.at[WeekDaysShort.th, OpenClose.open])

    @th_o.setter
    def th_o(self, data):
        self.__oh.at[WeekDaysShort.th, OpenClose.open] = data

    @property
    def fr_o(self):
        return (self.__oh.at[WeekDaysShort.fr, OpenClose.open])

    @fr_o.setter
    def fr_o(self, data):
        self.__oh.at[WeekDaysShort.fr, OpenClose.open] = data

    @property
    def sa_o(self):
        return (self.__oh.at[WeekDaysShort.sa, OpenClose.open])

    @sa_o.setter
    def sa_o(self, data):
        self.__oh.at[WeekDaysShort.sa, OpenClose.open] = data

    @property
    def su_o(self):
        return (self.__oh.at[WeekDaysShort.su, OpenClose.open])

    @su_o.setter
    def su_o(self, data):
        self.__oh.at[WeekDaysShort.su, OpenClose.open] = data

    @property
    def mo_c(self):
        return (self.__oh.at[WeekDaysShort.mo, OpenClose.close])

    @mo_c.setter
    def mo_c(self, data):
        self.__oh.at[WeekDaysShort.mo, OpenClose.close] = data

    @property
    def tu_c(self):
        return (self.__oh.at[WeekDaysShort.tu, OpenClose.close])

    @tu_c.setter
    def tu_c(self, data):
        self.__oh.at[WeekDaysShort.tu, OpenClose.close] = data

    @property
    def we_c(self):
        return (self.__oh.at[WeekDaysShort.we, OpenClose.close])

    @we_c.setter
    def we_c(self, data):
        self.__oh.at[WeekDaysShort.we, OpenClose.close] = data

    @property
    def th_c(self):
        return (self.__oh.at[WeekDaysShort.th, OpenClose.close])

    @th_c.setter
    def th_c(self, data):
        self.__oh.at[WeekDaysShort.th, OpenClose.close] = data

    @property
    def fr_c(self):
        return (self.__oh.at[WeekDaysShort.fr, OpenClose.close])

    @fr_c.setter
    def fr_c(self, data):
        self.__oh.at[WeekDaysShort.fr, OpenClose.close] = data

    @property
    def sa_c(self):
        return (self.__oh.at[WeekDaysShort.sa, OpenClose.close])

    @sa_c.setter
    def sa_c(self, data):
        self.__oh.at[WeekDaysShort.sa, OpenClose.close] = data

    @property
    def su_c(self):
        return (self.__oh.at[WeekDaysShort.su, OpenClose.close])

    @su_c.setter
    def su_c(self, data):
        self.__oh.at[WeekDaysShort.su, OpenClose.close] = data

    @property
    def summer_mo_o(self):
        return (self.__oh.at[WeekDaysShort.mo, OpenClose.summer_open])

    @summer_mo_o.setter
    def summer_mo_o(self, data):
        self.__oh.at[WeekDaysShort.mo, OpenClose.summer_open] = data

    @property
    def summer_tu_o(self):
        return (self.__oh.at[WeekDaysShort.tu, OpenClose.summer_open])

    @summer_tu_o.setter
    def summer_tu_o(self, data):
        self.__oh.at[WeekDaysShort.tu, OpenClose.summer_open] = data

    @property
    def summer_we_o(self):
        return (self.__oh.at[WeekDaysShort.we, OpenClose.summer_open])

    @summer_we_o.setter
    def summer_we_o(self, data):
        self.__oh.at[WeekDaysShort.we, OpenClose.summer_open] = data

    @property
    def summer_th_o(self):
        return (self.__oh.at[WeekDaysShort.th, OpenClose.summer_open])

    @summer_th_o.setter
    def summer_th_o(self, data):
        self.__oh.at[WeekDaysShort.th, OpenClose.summer_open] = data

    @property
    def summer_fr_o(self):
        return (self.__oh.at[WeekDaysShort.fr, OpenClose.summer_open])

    @summer_fr_o.setter
    def summer_fr_o(self, data):
        self.__oh.at[WeekDaysShort.fr, OpenClose.summer_open] = data

    @property
    def summer_sa_o(self):
        return (self.__oh.at[WeekDaysShort.sa, OpenClose.summer_open])

    @summer_sa_o.setter
    def summer_sa_o(self, data):
        self.__oh.at[WeekDaysShort.sa, OpenClose.summer_open] = data

    @property
    def summer_su_o(self):
        return (self.__oh.at[WeekDaysShort.su, OpenClose.summer_open])

    @summer_su_o.setter
    def summer_su_o(self, data):
        self.__oh.at[WeekDaysShort.su, OpenClose.summer_open] = data

    @property
    def summer_mo_c(self):
        return (self.__oh.at[WeekDaysShort.mo, OpenClose.summer_close])

    @summer_mo_c.setter
    def summer_mo_c(self, data):
        self.__oh.at[WeekDaysShort.mo, OpenClose.summer_close] = data

    @property
    def summer_tu_c(self):
        return (self.__oh.at[WeekDaysShort.tu, OpenClose.summer_close])

    @summer_tu_c.setter
    def summer_tu_c(self, data):
        self.__oh.at[WeekDaysShort.tu, OpenClose.summer_close] = data

    @property
    def summer_we_c(self):
        return (self.__oh.at[WeekDaysShort.we, OpenClose.summer_close])

    @summer_we_c.setter
    def summer_we_c(self, data):
        self.__oh.at[WeekDaysShort.we, OpenClose.summer_close] = data

    @property
    def summer_th_c(self):
        return (self.__oh.at[WeekDaysShort.th, OpenClose.summer_close])

    @summer_th_c.setter
    def summer_th_c(self, data):
        self.__oh.at[WeekDaysShort.th, OpenClose.summer_close] = data

    @property
    def summer_fr_c(self):
        return (self.__oh.at[WeekDaysShort.fr, OpenClose.summer_close])

    @summer_fr_c.setter
    def summer_fr_c(self, data):
        self.__oh.at[WeekDaysShort.fr, OpenClose.summer_close] = data

    @property
    def summer_sa_c(self):
        return (self.__oh.at[WeekDaysShort.sa, OpenClose.summer_close])

    @summer_sa_c.setter
    def summer_sa_c(self, data):
        self.__oh.at[WeekDaysShort.sa, OpenClose.summer_close] = data

    @property
    def summer_su_c(self):
        return (self.__oh.at[WeekDaysShort.su, OpenClose.summer_close])

    @summer_su_c.setter
    def summer_su_c(self, data):
        self.__oh.at[WeekDaysShort.su, OpenClose.summer_close] = data

    @property
    def lunch_break(self):
        return (self.__lunch_break['start'], self.__lunch_break['stop'])

    @lunch_break.setter
    def lunch_break(self, lunch_break_start, lunch_break_stop):
        self.__lunch_break = {'start': lunch_break_start, 'stop': lunch_break_stop}

    @property
    def lunch_break_start(self):
        return (self.__lunch_break['start'])

    @lunch_break_start.setter
    def lunch_break_start(self, data):
        self.__lunch_break['start'] = data

    @property
    def lunch_break_stop(self):
        return (self.__lunch_break['stop'])

    @lunch_break_stop.setter
    def lunch_break_stop(self, data):
        self.__lunch_break['stop'] = data


    def day_open(self, day, data):
        self.__oh.at[WeekDaysShort(day), OpenClose.open] = data

    def day_close(self, day, data):
        self.__oh.at[WeekDaysShort(day), OpenClose.close] = data

    @property
    def opening_hours(self):
        return (self.__opening_hours)

    @opening_hours.setter
    def opening_hours(self, data):
        self.__opening_hours = data

    def process_opening_hours(self):
        self.__oh = self.__oh.where((pd.notnull(self.__oh)), None)
        t = OpeningHours(self.__nonstop, self.__oh.at[WeekDaysShort.mo, OpenClose.open],
                         self.__oh.at[WeekDaysShort.tu, OpenClose.open],
                         self.__oh.at[WeekDaysShort.we, OpenClose.open],
                         self.__oh.at[WeekDaysShort.th, OpenClose.open],
                         self.__oh.at[WeekDaysShort.fr, OpenClose.open],
                         self.__oh.at[WeekDaysShort.sa, OpenClose.open],
                         self.__oh.at[WeekDaysShort.su, OpenClose.open],
                         self.__oh.at[WeekDaysShort.mo, OpenClose.close],
                         self.__oh.at[WeekDaysShort.tu, OpenClose.close],
                         self.__oh.at[WeekDaysShort.we, OpenClose.close],
                         self.__oh.at[WeekDaysShort.th, OpenClose.close],
                         self.__oh.at[WeekDaysShort.fr, OpenClose.close],
                         self.__oh.at[WeekDaysShort.sa, OpenClose.close],
                         self.__oh.at[WeekDaysShort.su, OpenClose.close],
                         self.__oh.at[WeekDaysShort.mo, OpenClose.summer_open],
                         self.__oh.at[WeekDaysShort.tu, OpenClose.summer_open],
                         self.__oh.at[WeekDaysShort.we, OpenClose.summer_open],
                         self.__oh.at[WeekDaysShort.th, OpenClose.summer_open],
                         self.__oh.at[WeekDaysShort.fr, OpenClose.summer_open],
                         self.__oh.at[WeekDaysShort.sa, OpenClose.summer_open],
                         self.__oh.at[WeekDaysShort.su, OpenClose.summer_open],
                         self.__oh.at[WeekDaysShort.mo, OpenClose.summer_close],
                         self.__oh.at[WeekDaysShort.tu, OpenClose.summer_close],
                         self.__oh.at[WeekDaysShort.we, OpenClose.summer_close],
                         self.__oh.at[WeekDaysShort.th, OpenClose.summer_close],
                         self.__oh.at[WeekDaysShort.fr, OpenClose.summer_close],
                         self.__oh.at[WeekDaysShort.sa, OpenClose.summer_close],
                         self.__oh.at[WeekDaysShort.su, OpenClose.summer_close],
                         self.__lunch_break['start'], self.__lunch_break['stop'])
        self.__opening_hours = t.process()

    def dump_opening_hours(self):
        print(self.__opening_hours)

    def add(self):
        self.process_opening_hours()
        self.process_geom()
        self.insert_data.append(
            [self.__code, self.__postcode, self.__city, self.__name, self.__branch, self.__website, self.__original, self.__street,
             self.__housenumber, self.__conscriptionnumber,
             self.__ref, self.__phone, self.__email, self.__geom, self.__nonstop, self.__oh.at[WeekDaysShort.mo, OpenClose.open],
             self.__oh.at[WeekDaysShort.tu, OpenClose.open],
             self.__oh.at[WeekDaysShort.we, OpenClose.open],
             self.__oh.at[WeekDaysShort.th, OpenClose.open],
             self.__oh.at[WeekDaysShort.fr, OpenClose.open],
             self.__oh.at[WeekDaysShort.sa, OpenClose.open],
             self.__oh.at[WeekDaysShort.su, OpenClose.open],
             self.__oh.at[WeekDaysShort.mo, OpenClose.close],
             self.__oh.at[WeekDaysShort.tu, OpenClose.close],
             self.__oh.at[WeekDaysShort.we, OpenClose.close],
             self.__oh.at[WeekDaysShort.th, OpenClose.close],
             self.__oh.at[WeekDaysShort.fr, OpenClose.close],
             self.__oh.at[WeekDaysShort.sa, OpenClose.close],
             self.__oh.at[WeekDaysShort.su, OpenClose.close],
             self.__oh.at[WeekDaysShort.mo, OpenClose.summer_open],
             self.__oh.at[WeekDaysShort.tu, OpenClose.summer_open],
             self.__oh.at[WeekDaysShort.we, OpenClose.summer_open],
             self.__oh.at[WeekDaysShort.th, OpenClose.summer_open],
             self.__oh.at[WeekDaysShort.fr, OpenClose.summer_open],
             self.__oh.at[WeekDaysShort.sa, OpenClose.summer_open],
             self.__oh.at[WeekDaysShort.su, OpenClose.summer_open],
             self.__oh.at[WeekDaysShort.mo, OpenClose.summer_close],
             self.__oh.at[WeekDaysShort.tu, OpenClose.summer_close],
             self.__oh.at[WeekDaysShort.we, OpenClose.summer_close],
             self.__oh.at[WeekDaysShort.th, OpenClose.summer_close],
             self.__oh.at[WeekDaysShort.fr, OpenClose.summer_close],
             self.__oh.at[WeekDaysShort.sa, OpenClose.summer_close],
             self.__oh.at[WeekDaysShort.su, OpenClose.summer_close], self.__lunch_break['start'], self.__lunch_break['stop'],
             self.__opening_hours])
        self.clear_all()

    def process(self):
        df = pd.DataFrame(self.insert_data)
        df.columns = POI_COLS
        return df.where((pd.notnull(df)), None)

    def lenght(self):
        return len(self.insert_data)