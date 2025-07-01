import requests
from datetime import datetime
import math
import smtplib
import time

MY_LAT =  32.795599
MY_LONG = -117.251172

my_email = "pythoncourse155@gmail.com"
my_password = 


# create a function to detect if the ISS is close to my current location
def iss_is_close():
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_data = iss_response.json()

    iss_lat = float(iss_data["iss_position"]["latitude"])
    iss_long = float(iss_data["iss_position"]["longitude"])

    if math.isclose(MY_LAT, iss_lat,abs_tol=5) and math.isclose(MY_LONG,iss_long,abs_tol=5):
        return True

# create a function to detect if it is currently nighttime

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json",params=parameters)

    response.raise_for_status()

    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])


    time_now = datetime.now()

    if time_now.hour > sunset or time_now.hour < sunrise:
        return True

# send me an email to tell me to go outside and look up
while True:
    # run the code every 60 seconds
    time.sleep(60)
    if iss_is_close() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(my_email,my_password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="tjsmelter@gmail.com",
                msg="Subject: Look Up \n\n"
                    "Go outside, the ISS is passing overhead")
