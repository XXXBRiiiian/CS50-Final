# CS50-Final
Final project of CS50

# Flight Logbook Web App
#### Video Demo:  <URL https://youtu.be/sdL-4gLmCps>
#### Description:

This project is a web-based flight logbook application built with Flask and SQLite. It allows pilots to log flight details, track their flight history, and manage their credentials securely.

## Features

- User registration and authentication (login/logout)
- Secure password hashing using `scrypt`
- CSRF protection with Flask-WTF
- Logbook entries for tracking flight details (date, model, flight time, landings, etc.)
- Pagination for flight history

## Technologies Used

- Python (Flask)
- SQLite (Database)
- Flask-WTF (Form handling and validation)
- CSRF protection
- Werkzeug for password hashing
- Bootstrap (for frontend styling)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/XXXBRiiiian/flight-logbook.git
   cd flight-logbook
   ```
2. Create a virtual environment and activate it:
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up the SQLite database:
   ```sh
   flask db init
   flask db migrate
   flask db upgrade
   ```
5. Run the Flask application:
   ```sh
   flask run
   ```

## Usage

- Visit `http://127.0.0.1:5000/` to access the logbook.
- Register a new user account.
- Log in to access and manage flight records.
- Add new flight logs and view flight history.

## Database Schema

### Users Table

| Column   | Type    | Description          |
|----------|-------- |----------------------|
| id       | Integer | Primary Key          |
| username | String  | Unique username      |
| hash     | String  | Hashed password      |
| hours    | Integer | Total flight hours   |
| minutes  | Integer | Total flight minutes |
| position | String  | Pilot's position     |

### History Table

| Column        | Type    | Description                        |
|---------------|-------- |------------------------------------|
| id            | Integer | Primary Key                        |
| user_id       | Integer | Foreign Key referencing `users.id` |
| date          | Date    | Flight date                        |
| model         | String  | Aircraft model                     |
| ident         | String  | Aircraft identification            |
| ap_from       | String  | Departure airport                  |
| ap_to         | String  | Arrival airport                    |
| hours         | Integer | Flight hours                       |
| minutes       | Integer | Flight minutes                     |
| night_hours   | Integer | Night flight hours                 |
| night_minutes | Integer | Night flight minutes               |
| land          | Integer | Number of landings                 |

## Contributing

Contributions are welcome! Feel free to fork this repository and submit a pull request.


## Author

Brian Tan - [GitHub Profile](https://github.com/XXXBRiiiian)

