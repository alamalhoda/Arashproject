import datetime

import jdatetime

shamsi_date = '1402/07/20'.split('/')
# if date[:4]<2000:
shamsi_date_year = int(shamsi_date[0])
shamsi_date_month = int(shamsi_date[1])
shamsi_date_day = int(shamsi_date[2])

gregorian_date = jdatetime.jalali.JalaliToGregorian(shamsi_date_year, shamsi_date_month, shamsi_date_day)
gregorian_date = datetime.date(gregorian_date.gyear, gregorian_date.gmonth, gregorian_date.gday)
print(type(gregorian_date))
print(gregorian_date)