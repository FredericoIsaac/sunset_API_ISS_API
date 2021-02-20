import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 38.722252
MY_LNG = -9.139337

MY_MAIL = "fake_mail@gmail.com"
PASSWORD = "fake_password"


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now_hour = datetime.now().hour

    if time_now_hour < sunrise or time_now_hour > sunset:
        return True
    else:
        return False


def is_iss_overhead():

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    # Handle status in case of Error
    response.raise_for_status()

    data = response.json()

    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])

    iss_position = (latitude, longitude)

    if (MY_LAT - 5.0 <= iss_position[0] <= MY_LAT + 5.0)\
            and (MY_LNG - 5.0 <= iss_position[1] <= MY_LNG + 5.0):
        return True
    else:
        return False


while True:
    if is_dark() and is_iss_overhead():

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()  # Encrypt mail
            connection.login(user=MY_MAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_MAIL,
                                to_addrs=MY_MAIL,
                                msg=f"Subject:ISS Overhead\n\nLook up!")
    time.sleep(60)

