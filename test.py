import pprint
import requests
import xlsxwriter
import urllib

url_1 = "https://maps.googleapis.com/maps/api/geocode/json?address={}"
url_2 = "https://api.openaq.org/v1/measurements?coordinates={}&radius=100000&limit=1"


def get_coordinates(place):
    print("running get_coordinates for {}".format(place))
    r = requests.get(url_1.format(place))
    data = r.json()
    if 'error_message' in data:
        print(data['error_message'])
        return None
    return data


def filter_geo(data):
    """Filters Google's Data for Geo locations"""
    print("running filter_geo")
    geo = data["results"][0]["geometry"]["location"]
    return geo


def get_air_quality(geo):
    """Given Geo location return from 3rd party API"""
    s = "{},{}".format(geo['lat'], geo['lng'])
    print("get_air_quality for {}".format(s))
    # print(s)
    r = requests.get(url_2.format(s))
    return r.json()


def filter_aq_data(data):
    """	Filter Air quality data"""
    print("filtering air quality data")
    r = u"{} {}".format(data["results"][0]["value"],
                        data["results"][0]["unit"])
    return {"air_quality": r}


def pizza(place):
    """
    This is the main worker function
         Input : place (string)
         Output : dictionary
    """

    geo_data = get_coordinates(place)
    if geo_data == None:
        return {}
    geo = filter_geo(geo_data)
    quality = get_air_quality(geo)
    return filter_aq_data(quality)


def write_to_csv(d):
    print("Creating /data.xlsx using data : \n{}".format(d))
    workbook = xlsxwriter.Workbook('data.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0

    for key in d.keys():
        row += 1
        worksheet.write(row, col, key)
        for item in d[key]:
            worksheet.write(row, col + 1, item)
            row += 1
    workbook.close()


def main():
    user_mapping = {}
    while True:
        s = input("\nEnter a City : ").replace(" ", "%20")
        if s == "stop":
            break
        r = pizza(s)
        if r == {}:
            continue
        user_mapping[s] = [r['air_quality']]
        print(r)
    write_to_csv(user_mapping)


if __name__ == "__main__":
    main()
