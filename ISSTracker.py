import requests
from datetime import datetime
import math
import smtplib
import time

# Location coordinates near to you
MY_LAT =  32.72107
MY_LONG = -117.16863

# Create log in credentials
my_email = "exampleaddress@yahoo.com"
my_password = 


# Create function to detect if the ISS is close to the current user location
def iss_is_close():
    # Call the ISS location API
    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_data = iss_response.json()

    # Pull ISS coordinates
    iss_lat = float(iss_data["iss_position"]["latitude"])
    iss_long = float(iss_data["iss_position"]["longitude"])

    # Check if ISS is within 5 degrees of the user location
    if math.isclose(MY_LAT, iss_lat,abs_tol=5) and math.isclose(MY_LONG,iss_long,abs_tol=5):
        return True

# Create a function to detect if it is currently nighttime at user location
def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }

    # Call sunrise-sunset API
    response = requests.get(url="https://api.sunrise-sunset.org/json",params=parameters)
    response.raise_for_status()
    data = response.json()

    # Pull sunrise and sunset hour
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # Get current time (local)
    time_now = datetime.now()

    # Return True if it is before sunrise or after sunset (i.e. night time)
    if time_now.hour > sunset or time_now.hour < sunrise:
        return True

# Create main loop to run the check continuously
while True:
    # run the code every 60 seconds
    time.sleep(60)
    # If ISS is close to and it is night at user location, send an automated email
    if iss_is_close() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(my_email,my_password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="tjsmelter@gmail.com",
                msg="Subject: Look Up \n\n"
                    "Go outside, the ISS is passing overhead")
