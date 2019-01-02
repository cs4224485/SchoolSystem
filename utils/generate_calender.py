import datetime
from utils.common import *

# 使用中国阴历计算的节日
CN_HOLIDAY = (('八月十五', '中秋节'), ('腊月三十', '除夕'), ('正月初一', '春节'), ('五月初五', '端午节'))
# 使用公历计算的节日
PUB_HOLIDAY = (('9-10', '教师节'), ('10-1', '国庆节'), ('1-1', '元旦'), ('4-5', '清明节'), ('5-1', '劳动节'))


class CalenderHandler(object):
    START_YEAR = 1901
    month_DAY_BIT = 12
    month_NUM_BIT = 13

    def is_leap_year(self, year):
        """
        判断闰年
        :param year:
        :return:
        """
        return year % 4 == 0 and year % 100 != 0 or year % 400 == 0

    def get_num_of_days_in_month(self, year, month):
        """
        获得每月的天数
        :param year:
        :param month:
        :return:
        """
        if month in (1, 3, 5, 7, 8, 10, 12):
            return 31
        elif month in (4, 6, 9, 11):
            return 30
        elif self.is_leap_year(year):
            return 29
        return 28

    def get_per_month_day(self):
        '''
        获取每月的日历
        :return:
        '''
        month_list = [9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8]
        current_month = datetime.datetime.today().month
        if current_month <= 8:
            years = [datetime.datetime.today().year - 1, datetime.datetime.today().year]
        else:
            years = [datetime.datetime.today().year, datetime.datetime.today().year + 1]
        year = years[0]
        calender_dict = {}
        for month in month_list:
            if month <= 8:
                year = years[1]
            month_day_num = self.get_num_of_days_in_month(year, month)
            for day in range(1, month_day_num + 1):
                if year not in calender_dict:
                    calender_dict[year] = {month: [day]}
                else:
                    if month not in calender_dict[year]:
                        calender_dict[year][month] = [day]
                    else:
                        calender_dict[year][month].append(day)
        return calender_dict

    def get_cn_holiday(self, cn_month, cn_day):
        '''
        通过阴历获取节日
        :param cn_month:
        :param cn_day:
        :return:
        '''
        day = '%s%s' % (cn_month, cn_day)
        for holiday in CN_HOLIDAY:
            if day == holiday[0]:
                return holiday[1]
        return None

    def get_pub_holiday(self, month, day):
        cal = "%s-%s" % (month, day)

        for holiday in PUB_HOLIDAY:
            if cal == holiday[0]:
                return holiday[1]
        return None

    def get_total_num_of_days(self, year, month):
        """
        获得1800年输入年月总天数
        :param year:
        :param month:
        :return:
        """
        days = 0
        for y in range(1800, year):
            if self.is_leap_year(y):
                days += 366
            else:
                days += 365

        for m in range(1, month):
            days += self.get_num_of_days_in_month(year, m)

        return days

    def get_start_day(self, year, month):
        """
        获得输入年月的第一天星期几
        :param year:
        :param month:
        :return:
        """
        day = (3 + self.get_total_num_of_days(year, month)) % 7
        if day == 0:
            day = 7
        return day

    def _cnDay(self, _day):
        """ 阴历-日
            Arg:
                type(_day) int 1 数字形式的阴历-日
            Return:
                String "初一"
        """
        _cn_day = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
                   "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "廿十",
                   "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
        return _cn_day[(_day - 1) % 30]

    def _cnMonth(self, _month):
        """ 阴历-月
            Arg:
                type(_day) int 13 数字形式的阴历-月
            Return:
                String "闰正月"
        """
        _cn_month = ["正月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "冬月", "腊月"]
        leap = (_month >> 4) & 0xf
        m = _month & 0xf
        _month = _cn_month[(m - 1) % 12]
        if leap == m:
            _month = "闰" + _month
        return _month

    def _cnMonthDays(self, _cn_year, _cn_month):
        """ 计算阴历月天数
            Arg:
                type(_cn_year) int 2018 数字年份
                type(_cn_month) int 6 数字阴历月份
            Return:
                int 30或29,该年闰月，闰月天数
        """
        # 农历数据 每个元素的存储格式如下：
        #   16~13    12          11~0
        #  闰几月 闰月日数  1~12月份农历日数
        _cn_month_list = [
            0x00752, 0x00ea5, 0x0ab2a, 0x0064b, 0x00a9b, 0x09aa6, 0x0056a, 0x00b59, 0x04baa, 0x00752,  # 1901 ~ 1910
            0x0cda5, 0x00b25, 0x00a4b, 0x0ba4b, 0x002ad, 0x0056b, 0x045b5, 0x00da9, 0x0fe92, 0x00e92,  # 1911 ~ 1920
            0x00d25, 0x0ad2d, 0x00a56, 0x002b6, 0x09ad5, 0x006d4, 0x00ea9, 0x04f4a, 0x00e92, 0x0c6a6,  # 1921 ~ 1930
            0x0052b, 0x00a57, 0x0b956, 0x00b5a, 0x006d4, 0x07761, 0x00749, 0x0fb13, 0x00a93, 0x0052b,  # 1931 ~ 1940
            0x0d51b, 0x00aad, 0x0056a, 0x09da5, 0x00ba4, 0x00b49, 0x04d4b, 0x00a95, 0x0eaad, 0x00536,  # 1941 ~ 1950
            0x00aad, 0x0baca, 0x005b2, 0x00da5, 0x07ea2, 0x00d4a, 0x10595, 0x00a97, 0x00556, 0x0c575,  # 1951 ~ 1960
            0x00ad5, 0x006d2, 0x08755, 0x00ea5, 0x0064a, 0x0664f, 0x00a9b, 0x0eada, 0x0056a, 0x00b69,  # 1961 ~ 1970
            0x0abb2, 0x00b52, 0x00b25, 0x08b2b, 0x00a4b, 0x10aab, 0x002ad, 0x0056d, 0x0d5a9, 0x00da9,  # 1971 ~ 1980
            0x00d92, 0x08e95, 0x00d25, 0x14e4d, 0x00a56, 0x002b6, 0x0c2f5, 0x006d5, 0x00ea9, 0x0af52,  # 1981 ~ 1990
            0x00e92, 0x00d26, 0x0652e, 0x00a57, 0x10ad6, 0x0035a, 0x006d5, 0x0ab69, 0x00749, 0x00693,  # 1991 ~ 2000
            0x08a9b, 0x0052b, 0x00a5b, 0x04aae, 0x0056a, 0x0edd5, 0x00ba4, 0x00b49, 0x0ad53, 0x00a95,  # 2001 ~ 2010
            0x0052d, 0x0855d, 0x00ab5, 0x12baa, 0x005d2, 0x00da5, 0x0de8a, 0x00d4a, 0x00c95, 0x08a9e,  # 2011 ~ 2020
            0x00556, 0x00ab5, 0x04ada, 0x006d2, 0x0c765, 0x00725, 0x0064b, 0x0a657, 0x00cab, 0x0055a,  # 2021 ~ 2030
            0x0656e, 0x00b69, 0x16f52, 0x00b52, 0x00b25, 0x0dd0b, 0x00a4b, 0x004ab, 0x0a2bb, 0x005ad,  # 2031 ~ 2040
            0x00b6a, 0x04daa, 0x00d92, 0x0eea5, 0x00d25, 0x00a55, 0x0ba4d, 0x004b6, 0x005b5, 0x076d2,  # 2041 ~ 2050
            0x00ec9, 0x10f92, 0x00e92, 0x00d26, 0x0d516, 0x00a57, 0x00556, 0x09365, 0x00755, 0x00749,  # 2051 ~ 2060
            0x0674b, 0x00693, 0x0eaab, 0x0052b, 0x00a5b, 0x0aaba, 0x0056a, 0x00b65, 0x08baa, 0x00b4a,  # 2061 ~ 2070
            0x10d95, 0x00a95, 0x0052d, 0x0c56d, 0x00ab5, 0x005aa, 0x085d5, 0x00da5, 0x00d4a, 0x06e4d,  # 2071 ~ 2080
            0x00c96, 0x0ecce, 0x00556, 0x00ab5, 0x0bad2, 0x006d2, 0x00ea5, 0x0872a, 0x0068b, 0x10697,  # 2081 ~ 2090
            0x004ab, 0x0055b, 0x0d556, 0x00b6a, 0x00752, 0x08b95, 0x00b45, 0x00a8b, 0x04a4f, ]
        if (_cn_year < self.START_YEAR):
            return 30

        leap_month, leap_day, month_day = 0, 0, 0  # 闰几月，该月多少天 传入月份多少天

        tmp = _cn_month_list[_cn_year - self.START_YEAR]

        if tmp & (1 << (_cn_month - 1)):
            month_day = 30
        else:
            month_day = 29

        # 闰月
        leap_month = (tmp >> self.month_NUM_BIT) & 0xf
        if leap_month:
            if (tmp & (1 << self.month_DAY_BIT)):
                leap_day = 30
            else:
                leap_day = 29

        return [month_day, leap_month, leap_day]

    def _getNumCnDate(self, _date):
        """ 获取数字形式的农历日期
            Args:
                _date = datetime(year, month, day)
            Return:
                _year, _month, _day
                返回的月份，高4bit为闰月月份，低4bit为其它正常月份
        """
        # 农历数据 每个元素的存储格式如下：
        # 7~6    5~1
        # 春节月  春节日
        _cn_year_list = [
            0x53, 0x48, 0x3d, 0x50, 0x44, 0x39, 0x4d, 0x42, 0x36, 0x4a,  # 1901 ~ 1910
            0x3e, 0x52, 0x46, 0x3a, 0x4e, 0x43, 0x37, 0x4b, 0x41, 0x54,  # 1911 ~ 1920
            0x48, 0x3c, 0x50, 0x45, 0x38, 0x4d, 0x42, 0x37, 0x4a, 0x3e,  # 1921 ~ 1930
            0x51, 0x46, 0x3a, 0x4e, 0x44, 0x38, 0x4b, 0x3f, 0x53, 0x48,  # 1931 ~ 1940
            0x3b, 0x4f, 0x45, 0x39, 0x4d, 0x42, 0x36, 0x4a, 0x3d, 0x51,  # 1941 ~ 1950
            0x46, 0x3b, 0x4e, 0x43, 0x38, 0x4c, 0x3f, 0x52, 0x48, 0x3c,  # 1951 ~ 1960
            0x4f, 0x45, 0x39, 0x4d, 0x42, 0x35, 0x49, 0x3e, 0x51, 0x46,  # 1961 ~ 1970
            0x3b, 0x4f, 0x43, 0x37, 0x4b, 0x3f, 0x52, 0x47, 0x3c, 0x50,  # 1971 ~ 1980
            0x45, 0x39, 0x4d, 0x42, 0x54, 0x49, 0x3d, 0x51, 0x46, 0x3b,  # 1981 ~ 1990
            0x4f, 0x44, 0x37, 0x4a, 0x3f, 0x53, 0x47, 0x3c, 0x50, 0x45,  # 1991 ~ 2000
            0x38, 0x4c, 0x41, 0x36, 0x49, 0x3d, 0x52, 0x47, 0x3a, 0x4e,  # 2001 ~ 2010
            0x43, 0x37, 0x4a, 0x3f, 0x53, 0x48, 0x3c, 0x50, 0x45, 0x39,  # 2011 ~ 2020
            0x4c, 0x41, 0x36, 0x4a, 0x3d, 0x51, 0x46, 0x3a, 0x4d, 0x43,  # 2021 ~ 2030
            0x37, 0x4b, 0x3f, 0x53, 0x48, 0x3c, 0x4f, 0x44, 0x38, 0x4c,  # 2031 ~ 2040
            0x41, 0x36, 0x4a, 0x3e, 0x51, 0x46, 0x3a, 0x4e, 0x42, 0x37,  # 2041 ~ 2050
            0x4b, 0x41, 0x53, 0x48, 0x3c, 0x4f, 0x44, 0x38, 0x4c, 0x42,  # 2051 ~ 2060
            0x35, 0x49, 0x3d, 0x51, 0x45, 0x3a, 0x4e, 0x43, 0x37, 0x4b,  # 2061 ~ 2070
            0x3f, 0x53, 0x47, 0x3b, 0x4f, 0x45, 0x38, 0x4c, 0x42, 0x36,  # 2071 ~ 2080
            0x49, 0x3d, 0x51, 0x46, 0x3a, 0x4e, 0x43, 0x38, 0x4a, 0x3e,  # 2081 ~ 2090
            0x52, 0x47, 0x3b, 0x4f, 0x45, 0x39, 0x4c, 0x41, 0x35, 0x49,  # 2091 ~ 2100
        ]
        _year, _month, _day = _date.year, 1, 1
        _code_year = _cn_year_list[_year - self.START_YEAR]
        """ 获取当前日期与当年春节的差日 """
        _span_days = (_date - datetime.datetime(_year, ((_code_year >> 5) & 0x3), ((_code_year >> 0) & 0x1f))).days
        # print("span_day: ", _span_days)

        if (_span_days >= 0):
            """ 新年后推算日期，差日依序减月份天数，直到不足一个月，剪的次数为月数，剩余部分为日数 """
            """ 先获取闰月 """
            _month_days, _leap_month, _leap_day = self._cnMonthDays(_year, _month)
            while _span_days >= _month_days:
                """ 获取当前月份天数，从差日中扣除 """
                _span_days -= _month_days
                if (_month == _leap_month):
                    """ 如果当月还是闰月 """
                    _month_days = _leap_day
                    if (_span_days < _month_days):
                        """ 指定日期在闰月中 ???"""
                        _month = (_leap_month << 4) | _month
                        break
                    """ 否则扣除闰月天数，月份加一 """
                    _span_days -= _month_days
                _month += 1
                _month_days = self._cnMonthDays(_year, _month)[0]
            _day += _span_days
            return _year, _month, _day
        else:
            """ 新年前倒推去年日期 """
            _month = 12
            _year -= 1
            _month_days, _leap_month, _leap_day = self._cnMonthDays(_year, _month)
            while abs(_span_days) > _month_days:
                _span_days += _month_days
                _month -= 1
                if (_month == _leap_month):
                    _month_days = _leap_day
                    if (abs(_span_days) <= _month_days):  # 指定日期在闰月中
                        _month = (_leap_month << 4) | _month
                        break
                    _span_days += _month_days
                _month_days = self._cnMonthDays(_year, _month)[0]
            _day += (_month_days + _span_days)  # 从月份总数中倒扣 得到天数
            return _year, _month, _day

    def getCnMonth(self, _date):
        """ 获取农历月份
            Args:
                _date = datetime(year, month, day)
            Return:
                "xx"
        """
        _month = self._getNumCnDate(_date)[1]
        return "%s" % self._cnMonth(_month)

    def getCnDay(self, _date):
        """ 获取农历日
            Args:
                _date = datetime(year, month, day)
            Return:
                "农历 xx[x]年 xxxx年x月xx 星期x"
        """
        _day = self._getNumCnDate(_date)[2]
        return "%s" % self._cnDay(_day)
