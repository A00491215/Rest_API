# Hotel Reservation System REST API

This is a REST API for a Hotel Reservation System developed using Django Rest Framework. It allows querying available hotels based on requested dates and creating hotel reservations with specific guests.

## Features
* Retrieve a list of available hotels for given check-in and check-out dates.
* Create a hotel reservation that includes associated guest details.
* The API utilizes SQLite as the persistence mechanism for simplicity and ease of testing.

## Prerequisites
* Python 3.9+
* pip

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd "Rest API"
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Load Initial Data (Optional):**
   Run the included script to pre-populate some hotels.
   ```bash
   python populate_db.py
   ```

6. **Run the Server:**
   ```bash
   python manage.py runserver
   ```
   The API will be available at `http://127.0.0.1:8000/`.

## API Documentation

### 1. Get List of Hotels
**Endpoint:** `GET /api/getListOfHotels/`

**Description:** Returns the list of hotels available in the system. The hotel list changes based on check-in or check-out dates (i.e., filters out hotels that have overlapping reservations). 

**Query Parameters:**
* `checkin` (string, format YYYY-MM-DD) - The required check-in date.
* `checkout` (string, format YYYY-MM-DD) - The required check-out date.

**Example Request:**
```
GET /api/getListOfHotels/?checkin=2026-04-10&checkout=2026-04-15
```

**Example Response:**
```json
[
    {
        "id": 1,
        "name": "The Grand Halifa",
        "base_price": "250.00"
    },
    ...
]
```

### 2. Reservation Confirmation
**Endpoint:** `POST /api/reservationConfirmation/`

**Description:** Creates a hotel reservation and returns a confirmation number. The guests list must be included and guests will be tied to the reservation.

**Headers:**
* `Content-Type: application/json`

**Example Request Body:**
```json
{
  "hotel_name": "The Grand Halifa",
  "checkin": "2026-04-10",
  "checkout": "2026-04-15",
  "guests_list": [
    {
      "guest_name": "John Doe",
      "gender": "Male"
    },
    {
      "guest_name": "Jane Doe",
      "gender": "Female"
    }
  ]
}
```

**Example Response:**
```json
{
    "confirmation_number": "54de69c8-d9d1-41ee-82c5-3c12f8623514"
}
```
