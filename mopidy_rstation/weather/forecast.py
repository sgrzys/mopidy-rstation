import urllib2
import sys
import json
import os
import time
import codecs
from mopidy_rstation.utils import Utils


class ForecastData:
    data = None
    conf = None
    verbose = False
    location_name = None
    country_name = None
    temp_file = None

    def __init__(self, conf):
        self.conf = conf
        self.temp_file = "/tmp/rstation.weather.cache" + \
            self.conf['location_gps']
        geo = self.geolookup()
        self.temp_file = self.temp_file + ".json"
        self.location_name = geo['location']['city']
        self.country_name = geo['location']['country_name']

        if os.path.exists(self.temp_file):
            age = time.time() - os.path.getmtime(self.temp_file)
            print('File age is: ' + str(age))
            # 60s - 1 minute
            if age > 60:
                if self.verbose:
                    print("Updating cache file")
                self.fetch_data()
            else:
                if self.verbose:
                    print("Cache file " + str(int(age)) + " seconds old.")
        else:
            self.fetch_data()

        try:
            f = codecs.open(self.temp_file, "r", "utf-8")
        except IOError:
            self.fetch_error()

        self.data = json.load(f)
        f.close()

    def geolookup(self):
        temp_file = self.temp_file + ".geo.json"
        if os.path.exists(temp_file):
            pass
        else:
            req = ("http://api.wunderground.com/api/" +
                   "%s/geolookup/lang:%s/q/%s.json"
                   % (self.conf['weather_api_key'],
                      self.conf['language'][3:],
                      urllib2.quote(self.conf['location_gps'])))
            try:
                response = urllib2.urlopen(req)
            except urllib2.URLError as e:
                if hasattr(e, 'reason') and self.verbose:
                    print(e.reason)
                elif hasattr(e, 'code') and self.verbose:
                    print("Status returned: " + str(e.code))

            json_data = response.read().decode('utf-8', 'replace')
            data = json.loads(json_data)

            try:
                print(data['response']['error']['description'])
            except KeyError:
                pass

            f = codecs.open(temp_file, "w", "utf-8")
            f.write(json_data)
            f.close()

            if self.verbose:
                print("Geo data fetched successfully")

        try:
            f = codecs.open(temp_file, "r", "utf-8")
        except IOError:
            self.fetch_error()

        data = json.load(f)
        f.close()

        return data

    def fetch_data(self):
        # Grab data from Weather Underground API
        req = ("http://api.wunderground.com/api/" +
               "%s/conditions/forecast/lang:%s/q/%s.json"
               % (self.conf['weather_api_key'],
                  self.conf['language'][3:],
                  urllib2.quote(self.conf['location_gps'])))

        if self.verbose:
            print("Fetching weather data...")

        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError as e:
            if hasattr(e, 'reason') and self.verbose:
                print(e.reason)
            elif hasattr(e, 'code') and self.verbose:
                print("Status returned: " + str(e.code))

        json_data = response.read().decode('utf-8', 'replace')
        data = json.loads(json_data)

        try:
            print(data['response']['error']['description'])
        except KeyError:
            pass

        f = codecs.open(self.temp_file, "w", "utf-8")
        f.write(json_data)
        f.close()

        if self.verbose:
            print("Data fetched successfully")

    def read_current(self):
        # Assign current conditions to a dictionary
        try:
            current = self.data['current_observation']
        except KeyError:
            self.fetch_error()

        # Collect and merge wind data
        wind_dir = current['wind_dir']
        wind_mph = current['wind_mph']
        wind = wind_dir + " " + str(int(round(float(wind_mph)))) + "mph"

        current_dict = {
            "condition": current['weather'],
            "temp_f": int(round(float(current['temp_f']))),
            "temp_c": int(round(float(current['temp_c']))),
            "humidity": current['relative_humidity'],
            "wind": wind,
            "pressure_mb": current['pressure_mb'],
            "pressure_in": current['pressure_in'],
            "dewpoint_c": current['dewpoint_c'],
            "dewpoint_f": current['dewpoint_f'],
            "heat_index_c": current['heat_index_c'],
            "heat_index_f": current['heat_index_f'],
            "windchill_c": current['windchill_c'],
            "windchill_f": current['windchill_f'],
            "feelslike_c": current['feelslike_c'],
            "feelslike_f": current['feelslike_f'],
            "visibility_mi": current['visibility_mi'],
            "visibility_km": current['visibility_km'],
            "prec_hour_in": current['precip_1hr_in'],
            "prec_hour_cm": current['precip_1hr_metric'],
            "prec_day_in": current['precip_today_in'],
            "prec_day_cm": current['precip_today_metric'],
        }

        return current_dict

    def read_simple_forecast(self):
        # Assign forecast to a dictionary
        forecast_dict = []

        try:
            forecast = self.data['forecast']['simpleforecast']['forecastday']
        except KeyError:
            self.fetch_error()

        count = 1

        for index, node in enumerate(forecast):

            d = node['date']

            conditions = {
                "day": d['weekday'],
                "shortdate": str(
                    d['month']) + "/" + str(d['day']) + "/" + str(d['year']),
                "longdate": d['monthname'] + " " + str(
                    d['day']) + ", " + str(d['year']),
                "low_f": node['low']['fahrenheit'],
                "low_c": node['low']['celsius'],
                "high_f": node['high']['fahrenheit'],
                "high_c": node['high']['celsius'],
                "condition": node['conditions'],
                "rain_in": node['qpf_allday']['in'],
                "rain_mm": node['qpf_allday']['mm'],
                "snow_in": node['snow_allday']['in'],
                "snow_cm": node['snow_allday']['cm'],
            }

            forecast_dict.append(conditions)
            count += 1

        return forecast_dict

    def read_txt_forecast(self):
        # Assign forecast to a dictionary
        forecast_dict = []

        try:
            forecast = self.data['forecast']['txt_forecast']['forecastday']
        except KeyError:
            self.fetch_error()

        count = 1

        for index, node in enumerate(forecast):
            conditions = {
                "title": node['title'],
                "text": node['fcttext_metric'],
            }
            forecast_dict.append(conditions)
            count += 1

        return forecast_dict

    def read_info(self):

        try:
            info = self.data['current_observation']
        except KeyError:
            self.fetch_error()

        info_dict = {
            "city": info['display_location']['city'],
            "postal": info['display_location']['zip'],
            "datetime": info['observation_time'],
            "location": info['display_location']['full'],
            "country": info['display_location']['country'],
            "latitude": info['display_location']['latitude'],
            "longitude": info['display_location']['longitude'],
            "elevation": info['display_location']['elevation'],
            "observation": info['observation_location']['full'],
        }
        return info_dict

    def fetch_error(self):
        e = "Data file has not been populated. Use 'pywu -v fetch \
            <apikey> <location>' first."
        if self.verbose:
            print(e)


def main():
    conf = Utils.get_config()

    # if the location is passed we will try to take geolookup the gps first
    # if len(sys.argv) > 1:
    #     .location = sys.argv[1]

    forecast = ForecastData(conf['rstation'])
    forecast.verbose = True
    print(forecast.location_name)
    print('----------------------------------')
    days = forecast.read_txt_forecast()
    for day in days:
        print(day)


if __name__ == '__main__':
    main()
    sys.exit()
