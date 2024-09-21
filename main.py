import requests
from datetime import datetime
import time
import smtplib

MY_LAT = 38.4186044  # Your latitude
MY_LONG = -27.1458787  # Your longitude

time_now = datetime.now()


def get_iss_location():
    res_iss = requests.get(url="http://api.open-notify.org/iss-now.json")
    res_iss.raise_for_status()
    res = res_iss.json()
    iss_latitude = float(res["iss_position"]["latitude"])
    iss_longitude = float(res["iss_position"]["longitude"])
    return iss_latitude, iss_longitude


def proximity_checker():
    coordinates = get_iss_location()
    lat_range = range(int(MY_LAT) - 5, int(MY_LAT) + 5)
    long_range = range(int(MY_LONG) - 5, int(MY_LONG) + 5)
    if coordinates[0] in lat_range and coordinates[1] in long_range:
        return True
    return False


def send_mail():
    print("Mail sent...")
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user="ferhatadibelli9@gmail.com", password="rhtqxhmmdhezofol")
        connection.sendmail(
            from_addr="ferhatadibelli9@gmail.com",
            to_addrs="ferhat@codeventure.co",
            msg="Subject:Hello \n\n This is ISS message"
        )


def dark_checker():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    dark = False
    if time_now.hour > sunset or time_now.hour < sunrise:
        dark = True
    return dark


while True:
    print("Running...")
    is_dark = dark_checker()
    close = proximity_checker()
    if is_dark and close:
        send_mail()

    time.sleep(60)
