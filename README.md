# WT Labs
Assignment 1
# 🚀 Space Bot API Investigation Sheet
**Total Marks: 40**
**TASK 1: Collect Required API Documentation**
This investigation sheet helps you gather key technical information from the three
APIs required for the Space Bot project: **Webex Messaging API**, **ISS Current
Location API**, **Weather API** and a **Geocoding API** , plus the Python time
module. Also furhter investigate the application of Web Architecture and MVC design
pattern in development of the Bot
---
## Webex Messaging API

**API Base URL:** `https://webexapis.com/v1/`

**Authentication Method:** Bearer token using the `Authorization` header.

**Endpoints used:**

- Get rooms: `GET /rooms`
- Get messages in a room: `GET /messages?roomId={roomId}`
- Send a message: `POST /messages`

**Required Headers:**

```http
Authorization: Bearer YOUR_WEBEX_ACCESS_TOKEN
Content-Type: application/json
```

**Example JSON request body for sending a message:**

```json
{
  "roomId": "Y2lzY29zcGFyazovL3VybjpURU F0NmV1LWNlbnRyYWYwMTV9rL1JPT00vNmM5ZjNhMDAtYzIyYy0xMWYxLWI0ZDctMjdlYjQ2YmI2ZDZm",
  "text": "Hello! This message was sent using the Webex API."
}
```

**Example JSON response for getting rooms:**

```json
{
  "items": [
    {
      "id": "Y2lzY29zcGFyazovL3VybjpURU F0NmV1LWNlbnRyYWYwMTV9rL1JPT00vNmM5ZjNhMDAtYzIyYy0xMWYxLWI0ZDctMjdlYjQ2YmI2ZDZm",
      "title": "Test Astrobot"
    }
  ]
}
```

The bot uses the Webex Messaging API to retrieve available rooms, read messages and send replies. The access token is used to authenticate requests. The room ID above should be replaced with the actual ID returned by the Webex API.

---
## ISS Current Location API.

**API Provider:** Open Notify

**API Base URL:** `http://api.open-notify.org`

**Endpoint for current ISS location:** `/iss-now.json`

**Full Endpoint URL:** `http://api.open-notify.org/iss-now.json`

**Authentication Method:** No API key is required.

**Testing Tool:** Postman

**Request Method:** GET

**Sample JSON Response:**

```json
{
  "message": "success",
  "timestamp": 1791364611,
  "iss_position": {
    "longitude": "-157.1391",
    "latitude": "-50.6018"
  }
}
```
---
## Geocoding API (4 marks)

**API Provider:** OpenWeatherMap

**API Base URL:** `https://api.openweathermap.org`

**Geocoding Endpoint:** `/geo/1.0/direct`

**Reverse Geocoding Endpoint:** `/geo/1.0/reverse`

**Authentication Method:** API key using the `appid` query parameter.

**Required Parameters:**
- Direct geocoding: `q` (location name), `appid` (API key).
- Reverse geocoding: `lat` (latitude), `lon` (longitude), `appid` (API key).

**Sample Direct Geocoding Request:**

`https://api.openweathermap.org/geo/1.0/direct?q=London&limit=1&appid=YOUR_OPENWEATHER_API_KEY`

**Sample Reverse Geocoding Request:**

`https://api.openweathermap.org/geo/1.0/reverse?lat=51.5072&lon=-0.1276&limit=1&appid=YOUR_OPENWEATHER_API_KEY`

**Sample JSON Response:**

```json
[
  {
    "name": "London",
    "lat": 51.5072,
    "lon": -0.1276,
    "country": "GB",
    "state": "England"
  }
]
```

---
## Weather API (3 marks)

**API Provider:** OpenWeatherMap

**API Base URL:** `https://api.openweathermap.org`

**Weather Endpoint:** `/data/2.5/weather`

**Authentication Method:** API key using the `appid` query parameter.

**Required Parameters:**
- `lat`: `51.5072`
- `lon`: `-0.1276`
- `appid`: OpenWeatherMap API key.

**Sample Request:**
`https://api.openweathermap.org/data/2.5/weather?lat=51.5072&lon=-0.1276&appid=YOUR_OPENWEATHER_API_KEY&units=metric`

**Sample JSON Response:**
```json
{
  "weather": [
    {
      "main": "Clouds",
      "description": "overcast clouds"
    }
  ],
  "main": {
    "temp": 12.5,
    "feels_like": 11.8,
    "humidity": 76
  },
  "name": "London"
}
```
## Epoch to Human Time Conversion (Python time module) (2 marks)
**Library used:** `datetime`

**Function used to convert epoch:** `datetime.fromtimestamp()`

**Sample Code:**
```python
from datetime import datetime

timestamp = 1791364611
human_time = datetime.fromtimestamp(timestamp)

print(human_time)
```

**Human-readable output:** `2026-10-07 12:56:51`

## Extended Feature API ( 3 marks)

**API Provider:** NASA Astronomy Picture of the Day (APOD)

**API Base URL:** `https://science.nasa.gov`

**Endpoint:** `/wp-json/wp/v2/apod-basic`

**HTTP Request Method:** GET

**Authentication Method:** No API key required for this endpoint.

**Sample Request:**
`https://science.nasa.gov/wp-json/wp/v2/apod-basic`

**Data Retrieved:** The API returns astronomy picture information, including the title, explanation and image URL.
```
|
---
## Evaluation – Web Architecture, MVC Design & Security
### Web Architecture – Client–Server Model

AstroBot uses Python to communicate with Webex and external APIs. The APIs return data in JSON format, which the bot processes and sends back to the user in Webex.

### Security Considerations

The bot uses a Webex token and an OpenWeatherMap API key. These should be kept private and not uploaded to GitHub. HTTPS is used to make API requests securely.

### RESTful API Usage and Error Handling

AstroBot uses GET requests to retrieve weather information, the ISS location and NASA images. It processes the JSON responses and displays the results in Webex. Error handling helps prevent problems when an API request fails.

### MVC Design Pattern

AstroBot uses some MVC principles. Python functions retrieve and process data, Webex displays the results, and the commandhandling logic decides which function to run based on the user's command.

---
### Web Architecture – Client–Server Model (3 marks)

AstroBot follows the client–server model. The user sends commands through Webex, and the Python bot processes them. It then requests information from APIs such as OpenWeatherMap and Open Notify. The results are sent back to the user through Webex.
- **Client:** Webex, where the user sends commands.
- **Servers:** AstroBot and the external API servers.
- **Data flow:** The user sends a command through Webex, AstroBot processes it, gets data from the relevant API and sends the result back to Webex.
**Block Diagram:**
text
User
  ↕
Webex
  ↕
AstroBot (Python)
  ↕
External APIs
(OpenWeatherMap, Open Notify, NASA)
```

#### Security Considerations: (3 marks )

AstroBot uses a Webex token and an OpenWeatherMap API key to access the services. I have not included my actual keys in the code to avoid exposing them. The bot processes commands such as `/weather London` to handle user requests. API rate limits should also be considered to avoid sending too many requests. Error handling helps the bot deal with failed API requests without crashing.

### RESTful API Usage in Your Application (3 marks )
In my AstroBot, I use GET requests to get information from APIs, such as weather details from OpenWeatherMap, the ISS location from Open Notify and pictures from NASA. I use POST requests to send messages to Webex.

The APIs return data in JSON format, which my Python code reads and uses to get the information needed. For example, the bot gets the weather details and sends them back to the user in Webex. The geocoding API is used to find the latitude and longitude of a place so the bot can get its weather information.

#### Security Considerations: (2 marks)

My AstroBot needs to handle API errors in case a request fails or returns unexpected data. Checking response status codes helps identify problems with API requests. The bot should also handle invalid responses safely and avoid making too many API calls in a short time to prevent reaching rate limits.
---
### MVC Design Pattern in AstroBot (3 Marks)
Component	Description and Example
Model	Gets and processes data from APIs, such as weather information from OpenWeatherMap.
View	Webex, where the user sees the bot's replies.
Controller	The Python code that checks commands like /weather London and calls the correct function.

---
### 🚀 Reflection and Evaluation ( 8 marks )
My AstroBot is designed to help the Astronomy Club get information about space and the weather through Webex. I think it meets the club’s needs because users can type commands such as `/weather London` and `/iss` to get information without having to search different websites themselves. The bot also includes a `/help` command to show users which commands are available. This makes it simple to use, even for someone who does not have much technical knowledge.

One design decision that worked well was using Python to connect the different APIs and Webex. Each API has a specific purpose. For example, OpenWeatherMap provides weather information, Open Notify provides the current location of the International Space Station, and NASA provides astronomy-related information. I also used the geocoding API to find the latitude and longitude of a location before getting its weather. Using JSON responses made it possible for my code to extract the information it needed and send it back to the user.

One of the main challenges was connecting the APIs correctly and understanding the information they returned. I had problems with the OpenWeatherMap API key at first, which caused an error response. I had to check the key and make sure the request included the correct parameters. Another challenge was understanding how to connect Webex with the Python code so that the bot could receive commands and send replies to the correct space. Testing each API separately helped me identify problems more easily.

I also identified security risks. The Webex access token and OpenWeatherMap API key could be misused if someone else obtained them. I have not included my actual keys in the code examples for the assignment, which helps avoid exposing them. In a real system, I would store them in environment variables instead of directly in the source code. API requests can also fail or return unexpected information, so the bot needs error handling to prevent it from crashing. I would also limit unnecessary API requests to avoid reaching rate limits.

In the future, I would improve AstroBot by adding more astronomy commands, such as information about planets and upcoming space events. I would also improve the error messages so users understand what went wrong. Another improvement would be allowing the bot to send astronomy pictures directly into Webex instead of only providing information or links. Overall, this project helped me understand how APIs work together and how Python can be used to create a useful bot for a real group of users.

### Total: /40

### References 
1. Webex for Developers (n.d.) *Rooms API*. Available at: https://developer.webex.com/docs/api/v1/rooms (Accessed: 14 October 2026).

   Explains how the bot accesses Webex spaces and their information.

2. OpenWeather (n.d.) *Current Weather Data*. Available at: https://openweathermap.org/api/current (Accessed: 14 October 2026).

   Explains how the bot retrieves current weather information.

3. OpenWeather (n.d.) *Geocoding API*. Available at: https://openweathermap.org/api/geocoding-api (Accessed: 21 October 2026).

   Explains how the bot converts city names into coordinates for weather requests.

4. Open Notify (n.d.) *ISS Current Location API*. Available at: http://api.open-notify.org/iss-now.json (Accessed: 21 October 2026).

   Provides the API used to retrieve the International Space Station’s current location.
  
5. Requests (n.d.) *Quickstart*. Available at: https://requests.readthedocs.io/en/latest/user/quickstart/ (Accessed: 18 October 2026).

   Provides Python example code for making GET and POST requests, handling API responses and working with JSON data.

6. Python Software Foundation (n.d.) *datetime — Basic date and time types*. Available at: https://docs.python.org/3/library/datetime.html (Accessed: 21 October 2026).

   Provides example code for converting timestamps into readable dates and times.

(image.png)