from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Name, Country
from .serializers import NameSerializer
from .services import get_nationalize_data, get_country_data


class NameLookupView(APIView):
    def get(self, request):
        name = request.query_params.get("name")
        if not name:
            return Response(
                {"detail": "Missing 'name' query parameter"},
                status=status.HTTP_400_BAD_REQUEST
            )

        recent_threshold = timezone.now() - timedelta(days=1)
        records = Name.objects.filter(name=name, last_accessed_at__gte=recent_threshold)

        if records.exists():
            serializer = NameSerializer(records, many=True)
            return Response(serializer.data)

        nationalize_data = get_nationalize_data(name)
        if not nationalize_data or not nationalize_data.get("country"):
            return Response(
                {"detail": f"No country data found for name '{name}'"},
                status=404
            )

        result = []

        for item in nationalize_data["country"]:
            code = item["country_id"]
            probability = item["probability"]

            country = Country.objects.filter(code=code).first()
            if not country:
                country_data = get_country_data(code)
                if not country_data:
                    continue
                country = Country.objects.create(**country_data)

            stat, created = Name.objects.get_or_create(
                name=name,
                country=country,
                defaults={"probability": probability}
            )
            if not created:
                stat.probability = probability
                stat.request_count += 1
                stat.save()

            result.append(stat)

        serializer = NameSerializer(result, many=True)
        return Response(serializer.data)


class PopularNamesView(APIView):
    def get(self, request):
        country_code = request.query_params.get("country")
        if not country_code:
            return Response(
                {"detail": "Missing 'country' query parameter"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            country = Country.objects.get(code=country_code)
        except Country.DoesNotExist:
            return Response(
                {
                    "detail": f"Country with code '{country_code}' not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        top_names = (
            Name.objects.filter(country=country)
            .values("name")
            .annotate(total_requests=Count("request_count"))
            .order_by("-total_requests")[:5]
        )

        if not top_names:
            return Response({"detail": f"No name data found for country '{country_code}'"}, status=404)

        return Response(top_names)
