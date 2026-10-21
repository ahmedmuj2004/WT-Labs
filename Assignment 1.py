
# Contains partially completed code with sections for you to complete
# IT IS MANDATORY TO USE THE RESOURCE PROVIDED
# The starter code is structured into functions and modules.
# Complete the missing sections while maintaining this modular design.
# Use Git for version control and commit changes regularly.

import requests
import json
import time
from datetime import datetime


def get_webex_token():
    choice = input("Use hard-coded Webex token? (y/n): ").lower()

    # Ask for the token rather than storing it in the source code.
    token = input("Enter your Webex Access Token: ").strip()

    if not token:
        print("Webex token cannot be empty.")
        return None

    if token.lower().startswith("bearer "):
        return token

    return f"Bearer {token}"


def get_api_key(prompt, hardcoded_key):
    # Ask for the API key rather than storing it in the source code.
    api_key = input(f"Enter your {prompt}: ").strip()

    if not api_key:
        print(f"{prompt} cannot be empty.")
        return None

    return api_key


def get_rooms(token):
    url = "https://webexapis.com/v1/rooms"
    headers = {"Authorization": token}

    try:
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            print("Error fetching rooms:", response.status_code)
            return []

        return response.json().get("items", [])

    except requests.RequestException as error:
        print("Error connecting to Webex:", error)
        return []


def print_rooms(rooms):
    for room in rooms:
        print(f"Room: {room.get('title')} | ID: {room.get('id')}")


def select_room(rooms):
    while True:
        name = input("Enter the Webex room name: ").strip()

        for room in rooms:
            if name.lower() in room.get("title", "").lower():
                print(f"Selected room: {room['title']}")
                return room["id"]

        print("Room not found. Please try again.")


def get_latest_message(token, room_id):
    url = "https://webexapis.com/v1/messages"
    params = {"roomId": room_id, "max": 1}
    headers = {"Authorization": token}

    try:
        response = requests.get(
            url, headers=headers, params=params, timeout=15
        )

        if response.status_code != 200:
            print("Error fetching messages:", response.status_code)
            return None, None

        data = response.json().get("items", [])

        if not data:
            return None, None

        latest = data[0]
        return latest.get("id"), latest.get("text", "")

    except requests.RequestException as error:
        print("Error retrieving messages:", error)
        return None, None


def send_message(token, room_id, message):
    url = "https://webexapis.com/v1/messages"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }

    data = {"roomId": room_id, "text": str(message)}

    try:
        response = requests.post(
            url, headers=headers, data=json.dumps(data), timeout=15
        )

        if response.status_code not in (200, 201):
            print("Error sending message:", response.status_code)
            print(response.text)

    except requests.RequestException as error:
        print("Error sending message:", error)


def get_city_coordinates(city, api_key):
    url = "https://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city, "limit": 1, "appid": api_key}

    try:
        response = requests.get(url, params=params, timeout=15)

        if response.status_code != 200:
            print("Error getting city coordinates:", response.status_code)
            return None

        data = response.json()
        return data[0] if data else None

    except requests.RequestException as error:
        print("Geocoding error:", error)
        return None


def get_weather(city, api_key):
    location = get_city_coordinates(city, api_key)

    if not location:
        return f"City '{city}' not found. Please check the spelling."

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": location["lat"],
        "lon": location["lon"],
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=15)

        if response.status_code != 200:
            print("Error getting weather:", response.status_code)
            return "Weather information could not be retrieved."

        weather = response.json()

        city_name = weather.get("name", city)
        country = weather.get("sys", {}).get("country", "")
        temperature = weather.get("main", {}).get("temp", "N/A")
        description = weather.get("weather", [{}])[0].get(
            "description", "Unknown"
        )
        humidity = weather.get("main", {}).get("humidity", "N/A")
        wind = weather.get("wind", {}).get("speed", "N/A")

        return (
            f"Weather for {city_name}, {country}:\n"
            f"Temperature: {temperature}°C\n"
            f"Conditions: {description}\n"
            f"Humidity: {humidity}%\n"
            f"Wind speed: {wind} m/s"
        )

    except requests.RequestException as error:
        print("Weather request error:", error)
        return "Unable to retrieve weather information."


def reverse_geocode(lat, lon, api_key):
    url = "https://api.openweathermap.org/geo/1.0/reverse"
    params = {
        "lat": lat,
        "lon": lon,
        "limit": 1,
        "appid": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=15)

        if response.status_code != 200:
            return None

        data = response.json()
        return data[0] if data else None

    except requests.RequestException as error:
        print("Reverse geocoding error:", error)
        return None


def get_iss_location(api_key):
    url = "http://api.open-notify.org/iss-now.json"

    try:
        response = requests.get(url, timeout=15)

        if response.status_code != 200:
            return "ISS location could not be retrieved."

        data = response.json()

        if data.get("message") != "success":
            return "ISS location service returned an error."

        # Extract latitude and longitude from the JSON response.
        position = data.get("iss_position", {})
        lat = position.get("latitude")
        lon = position.get("longitude")

        if lat is None or lon is None:
            return "ISS coordinates are unavailable."

        location = reverse_geocode(lat, lon, api_key)
        place = "Over Ocean / No Nearby City"

        if location:
            place = ", ".join(
                str(location[key])
                for key in ("name", "state", "country")
                if location.get(key)
            ) or place

        # Convert the Unix timestamp to a readable date and time.
        timestamp = data.get("timestamp")
        time_text = ""

        if timestamp:
            time_text = datetime.fromtimestamp(timestamp).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        return (
            f"Current ISS Location:\n"
            f"Latitude: {lat}\n"
            f"Longitude: {lon}\n"
            f"Nearby location: {place}\n"
            f"Time: {time_text}"
        )

    except (requests.RequestException, ValueError) as error:
        print("ISS request error:", error)
        return "Unable to retrieve ISS location."



# Get the NASA Astronomy Picture of the Day

def get_astronomy_picture():
    url = "https://science.nasa.gov/wp-json/wp/v2/apod-basic"

    try:
        response = requests.get(url, timeout=15)

        if response.status_code != 200:
            return "Sorry, NASA information is not available right now."

        data = response.json()

        # The API may return a list of pictures.
        if isinstance(data, list):
            if not data:
                return "No astronomy picture was found."
            data = data[0]

        title = data.get("title", "Astronomy Picture of the Day")
        explanation = data.get("explanation", "No description available.")
        image = data.get("url", data.get("hdurl", ""))

        return (
            f"NASA Astronomy Picture of the Day\n"
            f"Title: {title}\n"
            f"{explanation[:500]}\n"
            f"Picture: {image}"
        )

    except (requests.RequestException, ValueError) as error:
        print("NASA request error:", error)
        return "Could not retrieve NASA's astronomy picture."




def main():
    token = get_webex_token()

    if not token:
        return

    weather_key = get_api_key(
        "OpenWeather API key",
        "YOUR_OPENWEATHER_API_KEY"
    )

    if not weather_key:
        return

    rooms = get_rooms(token)

    if not rooms:
        print("No rooms found or Webex could not be reached.")
        return

    print_rooms(rooms)
    room_id = select_room(rooms)

    last_message_id, _ = get_latest_message(token, room_id)

    while True:
        message_id, message_text = get_latest_message(token, room_id)

        if message_id and message_id != last_message_id:
            last_message_id = message_id
            message_text = (message_text or "").strip()

            print("Received message:", message_text)

            if not message_text.startswith("/"):
                time.sleep(5)
                continue

            if message_text.lower() == "/help":
                send_message(
                    token,
                    room_id,
                    "Available commands:\n"
                    "/weather <city>\n"
                    "/iss\n"
                    "/stars\n"
                    "/help\n"
                    "/quit"
                )

            elif message_text.lower().startswith("/weather"):
                parts = message_text.split(maxsplit=1)

                if len(parts) < 2 or not parts[1].strip():
                    send_message(
                        token, room_id, "Usage: /weather <city>"
                    )
                else:
                    city = parts[1].strip()
                    send_message(
                        token, room_id, get_weather(city, weather_key)
                    )

            elif message_text.lower() == "/iss":
                send_message(
                    token, room_id, get_iss_location(weather_key)
                )

            elif message_text.lower() == "/stars":
                send_message(
                    token, room_id, get_astronomy_picture()
                )

            elif message_text.lower() == "/quit":
                send_message(
                    token, room_id, "AstroBot shutting down."
                )
                break

            else:
                send_message(
                    token, room_id, "Unknown command. Use /help"
                )

        time.sleep(5)


if __name__ == '__main__':
    main()
