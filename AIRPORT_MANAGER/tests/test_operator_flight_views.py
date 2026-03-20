from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model

from AIRPORT_MANAGER.models import (
    Flight, Airport, Crew, CrewRole, CrewMember, FlightCrew, Airline, Aircraft, UserRole, User
)
from AIRPORT_MANAGER.serializers import FlightSerializer




class OperatorFlightViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Създаване на тестов потребител оператор
        self.role = UserRole.objects.create(name="Inspector")
        self.operator = User.objects.create_user(username="operator", password="test123", role=self.role)
        self.airline = Airline.objects.create(name="Test Airline", country="Bulgaria")
        self.aircraft = Aircraft.objects.create(type="Boeing 737", capacity=200)

        # Създаване на летища
        self.airport_from = Airport.objects.create(name="Sofia Airport", city="Sofia", country="BG")
        self.airport_to = Airport.objects.create(name="London Heathrow", city="London", country="UK")

        # Създаване на полети - и двата полета са в една и съща бъдеща дата
        future_day = (now() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        self.future_day = future_day

        self.flight1 = Flight.objects.create(
            flight_number="BG123",
            departure_time=future_day + timedelta(hours=5),
            arrival_time=future_day + timedelta(hours=8),
            duration=timedelta(hours=3),
            price=250.00,
            flight_type="Passenger",
            status="On Time",
            from_airport=self.airport_from,
            to_airport=self.airport_to,
            airline=self.airline,
            aircraft=self.aircraft
        )

        self.flight2 = Flight.objects.create(
            flight_number="BG200",
            departure_time=future_day + timedelta(hours=10),
            arrival_time=future_day + timedelta(hours=13),
            duration=timedelta(hours=3),
            price=180.00,
            flight_type="Passenger",
            status="Delayed",
            from_airport=self.airport_from,
            to_airport=self.airport_to,
            airline=self.airline,
            aircraft=self.aircraft
        )

    # Търсене на полети
    def test_search_by_destination(self):
        response = self.client.get("/api/flights/?destination=London")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["flight_number"], "BG123")

    def test_search_by_departure_date(self):
        departure_date = self.future_day.date().isoformat()
        response = self.client.get(f"/api/flights/?departure_date={departure_date}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["flight_number"], "BG123")

    def test_search_invalid_destination(self):
        response = self.client.get("/api/flights/?destination=Atlantis")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_search_without_filters_returns_all(self):
        response = self.client.get("/api/flights/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    #Преглеждане и модифициране на плети
    def test_operator_can_view_flight_details(self):
        response = self.client.get(f"/api/flights/{self.flight1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["flight_number"], "BG123")

    def test_operator_can_edit_flight(self):
        self.client.force_authenticate(user=self.operator)
        updated_data = {
            "flight_number": "BG321",
            "price": 300.00,
            "status": "Delayed"
        }
        response = self.client.patch(f"/api/flights/{self.flight1.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка дали полета е обновен
        self.flight1.refresh_from_db()
        self.assertEqual(self.flight1.flight_number, "BG321")
        self.assertEqual(self.flight1.price, 300.00)
        self.assertEqual(self.flight1.status, "Delayed")

    def test_unauthorized_user_cannot_edit_flight(self):
        updated_data = {"price": 400.00}
        response = self.client.patch(f"/api/flights/{self.flight1.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
