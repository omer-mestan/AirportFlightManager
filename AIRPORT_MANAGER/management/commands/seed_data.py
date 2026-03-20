from django.core.management.base import BaseCommand
from AIRPORT_MANAGER.models import *
from faker import Faker
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = "Seeds the database with fake test data."

    def handle(self, *args, **options):
        fake = Faker()
        self.stdout.write("📦 Seeding test data...")

        # Roles
        user_roles = ['Admin', 'Student', 'Inspector']
        crew_roles = ['Pilot', 'Co-Pilot', 'Engineer', 'Attendant']

        for role in user_roles:
            UserRole.objects.get_or_create(name=role)

        for role in crew_roles:
            CrewRole.objects.get_or_create(name=role)

        # Users
        for _ in range(100):
            User.objects.create(
                name=fake.name(),
                email=fake.unique.email(),
                role=UserRole.objects.order_by('?').first(),
                password="test1234"
            )

        # Airports
        airports = []
        for _ in range(100):
            airport = Airport.objects.create(
                name=f"{fake.city()} International Airport",
                city=fake.city(),
                country=fake.country()
            )
            airports.append(airport)

        # Airlines
        airlines = []
        for _ in range(10):
            airline = Airline.objects.create(
                name=fake.company(),
                country=fake.country()
            )
            airlines.append(airline)

        # Aircrafts
        aircrafts = []
        for _ in range(20):
            aircraft = Aircraft.objects.create(
                type=f"{fake.word().capitalize()} {random.randint(100, 999)}",
                capacity=random.randint(100, 300)
            )
            aircrafts.append(aircraft)

        # Crews
        crews = []
        for _ in range(20):
            crew = Crew.objects.create()
            crews.append(crew)

        # Crew Members
        crew_members = []
        for _ in range(100):
            member = CrewMember.objects.create(
                name=fake.name(),
                role=CrewRole.objects.order_by('?').first(),
                crew=random.choice(crews)
            )
            crew_members.append(member)

        # Stopovers
        stopovers = []
        for _ in range(50):
            stop = Stopover.objects.create(
                airport=random.choice(airports)
            )
            stopovers.append(stop)

        # Flights
        flights = []
        for _ in range(50):
            from_airport = random.choice(airports)
            to_airport = random.choice(airports)
            while to_airport == from_airport:
                to_airport = random.choice(airports)

            departure = timezone.now() + timedelta(days=random.randint(1, 30))
            arrival = departure + timedelta(hours=random.randint(2, 12))

            flight = Flight.objects.create(
                flight_number=f"{fake.random_uppercase_letter()}{fake.random_uppercase_letter()}{random.randint(100,999)}",
                departure_time=departure,
                arrival_time=arrival,
                duration=arrival - departure,
                price=round(random.uniform(80, 500), 2),
                flight_type=random.choice(["Passenger", "Cargo"]),
                status=random.choice(["On Time", "Delayed", "Cancelled"]),
                aircraft=random.choice(aircrafts),
                crew=random.choice(crews),
                airline=random.choice(airlines),
                stopover=random.choice(stopovers),
                from_airport=from_airport,
                to_airport=to_airport,
            )
            flights.append(flight)

        # FlightCrew
        for _ in range(150):
            FlightCrew.objects.get_or_create(
                flight=random.choice(flights),
                member=random.choice(crew_members)
            )

        self.stdout.write(self.style.SUCCESS("✅ Seeding complete! 100 users, 20 crews, 50 flights, 100 airports, etc."))
