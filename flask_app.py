from flask import Flask
from flask import request
import requests,json,logging
from geopy.distance import geodesic

app = Flask(__name__)

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename='/home/mekinci/mysite/static/neuro_case.log',filemode='w') #logging configuration

def is_inside(spec, mkad):
    lower_corner = mkad["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["boundedBy"]["Envelope"]["lowerCorner"] #The borders of the lower-left and
    upper_corner = mkad["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["boundedBy"]["Envelope"]["upperCorner"]#upper-right corners of the area of the MKAD
    spec_coordinates = spec["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]#coordinates of the specified address
    if lower_corner.split()[0]< spec_coordinates.split()[0]<upper_corner.split()[0] and lower_corner.split()[1]<spec_coordinates.split()[1]<upper_corner.split()[1]: #are the latitude and longitude of the specified address between the latitude and longitude of the MKAD?
        return True
def calculate_distance(spec,mkad):
    mkad_lat = float(mkad["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split()[1])#The coordinate structure in the API response is "longitude latitude"
    mkad_lng = float(mkad["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split()[0])#Use space as separator and we have a list like ["longitude","latitude"]
    spec_lat = float(spec["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split()[1])#Swap latitude and longitude for geodesic function
    spec_lng = float(spec["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split()[0])#Convert strings to float and assign each value to variables
    return str(geodesic((mkad_lat,mkad_lng),(spec_lat,spec_lng)).km) #Convert float output from geodesic function to string for readability
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return 'This is a case study for neuro.net' #If request method is get give information about application
    if request.method == "POST":
        params = {
        'apikey': '*****',                               #Geocoder
        'geocode': 'MKAD',                               #API
        'lang': 'en_RU',                                 #Required
        'format':'json'                                  #Parameters for the MKAD's informations
        }
        mkad_response = requests.get('https://geocode-maps.yandex.ru/1.x', params).json()#api request for the MKAD's informations
        data = request.form #get the specified address which is received by http request
        params['geocode'] = data["address"]#Change geocode parameter to get API response for specified address
        spec_address_response = requests.get('https://geocode-maps.yandex.ru/1.x', params).json()#api request for the specified address
        if is_inside(spec_address_response,mkad_response): # call is_inside function to check if the specified address is located inside the MKAD
            logging.info("The address you entered is located inside the MKAD") # add the result to the log file
            return "The address you entered is located inside the MKAD"#show the result from terminal
        else:#The specified address is not located inside the MKAD, so call calculate_distance function to calculate the distance from the Moscow Ring Road to the specified address
            logging.info("The distance from the Moscow Ring Road to the specified address is: " + calculate_distance(spec_address_response,mkad_response) + " km") #add the result to the log file
            return "The distance from the Moscow Ring Road to the specified address is: " + calculate_distance(spec_address_response,mkad_response) + " km"#show the result from terminal
