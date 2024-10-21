# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests
import json


def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text
    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    ...

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    # 解析 JSON 数据
    if response.status_code == 200:
        data = response.json()  # 将响应内容解析为 JSON 字典
        return data
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None
    

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return len(data['features']) if data else 0


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake['properties']['mag']

def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    coordinates = earthquake['geometry']['coordinates']
    return coordinates[1], coordinates[0]  # 返回纬度和经度（忽略高度）


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    max_earthquake = max(data['features'], key=get_magnitude)  # 使用 key 函数找到最大震级的地震
    max_magnitude = get_magnitude(max_earthquake)
    max_location = get_location(max_earthquake)
    return max_magnitude, max_location


# With all the above functions defined, we can now call them and get the result
data = get_data()

if data:
  print(f"Loaded {count_earthquakes(data)}")
  max_magnitude, max_location = get_maximum(data)
  print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")
else:
  print("No data loaded")





from datetime import date
import matplotlib.pyplot as plt


def get_data():
    """Retrieve the data we will be working with."""
    import requests
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None


def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    year = date.fromtimestamp(timestamp/1000).year
    return year


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake['properties']['mag']


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    magnitudes_by_year = {}
    for earthquake in earthquakes:
        year = get_year(earthquake)
        magnitude = get_magnitude(earthquake)
        
        if year not in magnitudes_by_year:
            magnitudes_by_year[year] = []
        magnitudes_by_year[year].append(magnitude)
    return magnitudes_by_year

def plot_average_magnitude_per_year(earthquakes):
    """Plot the average magnitude of earthquakes per year."""
    magnitudes_by_year = get_magnitudes_per_year(earthquakes)
    
    years = sorted(magnitudes_by_year.keys())
    avg_magnitudes = [sum(magnitudes_by_year[year]) / len(magnitudes_by_year[year]) for year in years]
    
    plt.plot(years, avg_magnitudes, marker='o', color='orange')
    plt.title('Average Magnitude per Year')
    plt.xlabel('Year')
    plt.ylabel('Average Magnitude')
    plt.show()


def plot_number_per_year(earthquakes):
    """Plot the number of earthquakes per year."""
    magnitudes_by_year = get_magnitudes_per_year(earthquakes)
    
    years = sorted(magnitudes_by_year.keys())
    counts = [len(magnitudes_by_year[year]) for year in years]
    
    plt.plot(years, counts, marker='o')
    plt.title('Number of Earthquakes per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Earthquakes')
    plt.show()



# Get the data we will work with
data = get_data()
if data:
   quakes = get_data()['features']

# Plot the results - this is not perfect since the x axis is shown as real
# numbers rather than integers, which is what we would prefer!
   plot_number_per_year(quakes)
   plt.clf()  # This clears the figure, so that we don't overlay the two plots
   plot_average_magnitude_per_year(quakes)
else:
    print("Load data failed")