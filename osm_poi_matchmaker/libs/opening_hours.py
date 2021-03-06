# -*- coding: utf-8 -*-

try:
    import logging
    import sys
    import collections
    import pandas as pd
except ImportError as err:
    logging.error('Error %s import module: %s', __name__, err)
    logging.exception('Exception occurred')

    sys.exit(128)


class OpeningHours(object):

    def __init__(self, non_stop, mo_o, tu_o, we_o, th_o, fr_o, sa_o, su_o, mo_c, tu_c, we_c, th_c,
                 fr_c, sa_c, su_c, summer_mo_o, summer_tu_o, summer_we_o, summer_th_o, summer_fr_o,
                 summer_sa_o, summer_su_o, summer_mo_c, summer_tu_c, summer_we_c, summer_th_c,
                 summer_fr_c, summer_sa_c, summer_su_c, lb_start, lb_stop, public_holiday_open=None):
        self.__non_stop = non_stop
        self.opening_hours = {'mo': [mo_o, mo_c, summer_mo_o, summer_mo_c, 0],
                              'tu': [tu_o, tu_c, summer_tu_o, summer_tu_c, 1],
                              'we': [we_o, we_c, summer_we_o, summer_we_c, 2],
                              'th': [th_o, th_c, summer_th_o, summer_th_c, 3],
                              'fr': [fr_o, fr_c, summer_fr_o, summer_fr_c, 4],
                              'sa': [sa_o, sa_c, summer_sa_o, summer_sa_c, 5],
                              'su': [su_o, su_c, summer_su_o, summer_su_c, 6]}
        self.__lunch_break_start = lb_start
        self.__lunch_break_stop = lb_stop
        self.week_days = {0: 'mo', 1: 'tu', 2: 'we', 3: 'th', 4: 'fr', 5: 'sa', 6: 'su'}
        self.oh_types = ('open', 'close', 'summer_open', 'summer_close', 'did')
        self.df_oh = pd.DataFrame.from_dict(self.opening_hours, orient='index', columns=self.oh_types)
        self.df_dup = self.df_oh.sort_values('did').drop_duplicates(['open', 'close'], keep='first')
        self.df_dup['same'] = None
        self.__public_holiday_open = public_holiday_open
        for k, v in self.df_dup.iterrows():
            same = self.df_oh.loc[
                (self.df_oh['open'] == v['open']) & (self.df_oh['close'] == v['close'])].index.tolist()
            if same is not None:
                same_id = self.df_oh.loc[(self.df_oh['open'] == v['open']) & (self.df_oh['close'] == v['close'])][
                    'did'].tolist()
                self.df_dup.at[k, 'same'] = collections.OrderedDict(zip(same_id, same))

    @property
    def nonstop(self):
        return self.__non_stop

    @nonstop.setter
    def nonstop(self, value):
        self.__non_stop = value

    @property
    def public_holiday_open(self):
        return self.__public_holiday_open

    @public_holiday_open.setter
    def public_holiday_open(self, value):
        self.__public_holiday_open = value

    @property
    def lunch_break_start(self) -> str:
        """Get lunch break start for opening hours

        Returns:
            str: Stored value of launch break start, value like '12:00'
        """
        return self.__lunch_break_start

    @lunch_break_start.setter
    def lunch_break_start(self, value: str):
        """Set lunch break start for opening hours

        Args:
            data (str): Store value of launch break start with value like '12:00'
        """
        self.__lunch_break_start = value

    @property
    def lunch_break_stop(self) -> str:
        """Get lunch break stop for opening hours

        Returns:
            str: Stored value of launch break stop, value like '12:30'
        """
        return self.__lunch_break_stop

    @lunch_break_stop.setter
    def lunch_break_stop(self, value: str):
        """Set lunch break stop for opening hours

        Args:
            data (str): Store value of launch break stop with value like '12:30'
        """
        self.__lunch_break_stop = value

    def process(self):
        oh = ''
        oh_list = []
        for k, v in self.df_dup.iterrows():
            if v['open'] is not None and v['close'] is not None:
                # Order by week days
                ordered = collections.OrderedDict(sorted(v['same'].items(), key=lambda x: x[0]))
                same = list(ordered.values())
                # Public Holidays
                if self.__public_holiday_open is None:
                    oh_ph = ''
                elif self.__public_holiday_open is True:
                    oh_ph = '; PH on'
                elif self.__public_holiday_open is False:
                    oh_ph = '; PH off'
                else:
                    oh_ph = ''
                # Try to merge days interval
                if len(ordered) >= 2:
                    same_id = list(ordered.keys())
                    diffs = [same_id[i + 1] - same_id[i] for i in range(len(same_id) - 1)]
                    # Diffs list contains only 1 to make day interval
                    if diffs.count(1) == len(diffs):
                        days = '{}-{}'.format(list(ordered.values())[0], list(ordered.values())[-1])
                    # Make list of days
                    else:
                        days = ','.join(same)
                # Make list of days
                else:
                    days = ','.join(same)
                if self.__lunch_break_start is None and self.__lunch_break_stop is None:
                    # If open and close are equals we handles as closed
                    if self.df_dup.at[k, 'open'] != self.df_dup.at[k, 'close']:
                        oh_list.append(
                            '{} {}-{}'.format(days.title(), self.df_dup.at[k, 'open'], self.df_dup.at[k, 'close']))
                else:
                    # If open and close are equals we handles as closed
                    if self.df_dup.at[k, 'open'] != self.df_dup.at[k, 'close']:
                        oh_list.append(
                            '{} {}-{},{}-{}'.format(days.title(), self.df_dup.at[k, 'open'], self.__lunch_break_start,
                                                    self.__lunch_break_stop, self.df_dup.at[k, 'close']))
                oh = '; '.join(oh_list)
                oh = oh + oh_ph
        if self.__non_stop is True or 'Mo-Su 00:00-24:00' in oh:
            try:
                return '24/7{}'.format(oh_ph)
            except:
                return '24/7'
        elif oh_list == []:
            return None
        else:
            return oh
