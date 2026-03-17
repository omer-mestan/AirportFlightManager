# AirportFlightManager

AirportFlightManager is a Django REST Framework project for managing and searching airport flight data. It was created as a backend-focused academic team project and is designed around realistic airport workflows such as flight search, crew-related views, operator permissions, and role-based access to flight information.

The project is especially useful as a portfolio piece because it combines API development, custom permissions, data modeling, and automated testing in one structured application.

## Project Overview

The system provides different views of flight data depending on the type of user.

- passengers can search for flights by destination or flight number
- crew members can view flights assigned to them
- operators and inspectors can manage flight data with restricted write access
- administrators have full access to the system

This makes the project a good example of a backend service that is not only about CRUD, but also about business rules and access control.

## Main Features

- public flight listing and search
- flight filtering by destination and flight number
- crew-specific flight endpoint
- role-based write permissions
- administrative management of flights and related entities
- support for airports, flights, crew members, roles, and operators
- automated tests for search and permission-related behavior
- seed commands for sample data

## User Roles

The system is built around several roles:

- `Admin` - full system access
- `Inspector` - write access to flight-related data
- `CrewMember` - access to assigned or relevant crew flight information
- `Passenger` / public user - read-only flight search and view access

Custom permission logic is implemented in:

- `AIRPORT_MANAGER/permissions.py`

## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite
- Django test framework
- Behave / BDD-style feature files

## Repository Structure

Important files and folders include:

- `manage.py` - Django entry point
- `requirements.txt` - project dependencies
- `AIRPORT_MANAGER/models/Models.py` - core data models
- `AIRPORT_MANAGER/views/` - API view logic
- `AIRPORT_MANAGER/serializers/` - serializer definitions
- `AIRPORT_MANAGER/tests/` - automated tests
- `AIRPORT_MANAGER/features/` - feature-based test scenarios
- `AIRPORT_MANAGER/management/commands/` - seed commands
- `class_diagram.png` - class diagram for the project

## API Endpoints

The main API routes are defined in:

- `AIRPORT_MANAGER/urls.py`

Examples of available endpoints:

- `GET /api/flights/` - list flights
- `GET /api/flights/?destination=London` - search flights by destination
- `GET /api/flights/?flight_number=BG123` - search flights by flight number
- `GET /api/my-crew-flights/` - crew-specific upcoming flights

Depending on the endpoint and HTTP method, access may be public, restricted to authenticated crew members, or limited to admin / inspector roles.

## Data Model

The project includes entities related to airport operations, such as:

- airports
- flights
- users
- crew members
- roles
- operators

These models work together to support both public flight search and role-specific operational views.

## Testing

The repository contains multiple automated tests that cover important backend behavior, including:

- flight search by destination
- flight search by flight number
- invalid search scenarios
- crew flight scenarios
- operator-related flight views

Run the tests with:

```bash
python manage.py test
```

## Setup And Run

To run the project locally:

```bash
git clone https://github.com/omer-mestan/AirportFlightManager.git
cd AirportFlightManager
python -m venv venv
```

Activate the environment:

Windows:

```bash
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

Install dependencies and start the project:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

If you want sample data, you can also explore the available custom management commands inside:

- `AIRPORT_MANAGER/management/commands/`

## Documentation And Supporting Files

The repository also contains additional academic and project documentation, including:

- `class_diagram.png`
- project archives
- Word and ZIP documentation files related to the coursework

These files help document both the architecture and the educational context of the project.

## Why This Project Matters

AirportFlightManager is a strong backend-focused example because it shows more than basic endpoint creation. It demonstrates:

- relational data modeling
- API design with Django REST Framework
- role-based authorization
- project organization in Django
- automated testing
- domain-specific business logic in a realistic scenario

It also serves as a useful foundation for more advanced airport management systems, such as dashboard-based full-stack applications.

## Possible Future Improvements

Some directions for future development could include:

- JWT authentication
- Swagger / OpenAPI documentation
- frontend dashboard integration
- pagination and more advanced filtering
- deployment configuration
- Docker setup
- stronger test coverage and CI integration

## Authors

- Yumer Mestan
- Hristo Stoilov
- Aleks Tenev
- Dimitar Georgiev

## License

This project is published for educational purposes and is licensed under:

**Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**

More details:

- [https://creativecommons.org/licenses/by-nc/4.0/](https://creativecommons.org/licenses/by-nc/4.0/)
