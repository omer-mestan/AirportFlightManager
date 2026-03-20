from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from AIRPORT_MANAGER.models import Flight
from AIRPORT_MANAGER.serializers.FlightSerializer import FlightSerializer
from AIRPORT_MANAGER.permissions import IsAdminOrInspectorForWrite
from django.utils.dateparse import parse_time


class FlightViewSet(viewsets.ModelViewSet):
    serializer_class = FlightSerializer
    queryset = Flight.objects.select_related('to_airport', 'from_airport', 'airline')
    permission_classes = [IsAdminOrInspectorForWrite]

    def get_queryset(self):
        queryset = self.queryset
        params = self.request.query_params

        flight_number = params.get('flight_number')
        destination = params.get('destination')
        departure_after = params.get('departure_after')
        departure_before = params.get('departure_before')

        if flight_number:
            queryset = queryset.filter(flight_number__icontains=flight_number)
        if destination:
            queryset = queryset.filter(to_airport__name__icontains=destination)
        if departure_after:
            t = parse_time(departure_after)
            if t:
                queryset = queryset.filter(departure_time__time__gte=t)
        if departure_before:
            t = parse_time(departure_before)
            if t:
                queryset = queryset.filter(departure_time__time__lte=t)

        return queryset
