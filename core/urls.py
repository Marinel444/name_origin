from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import NameLookupView, PopularNamesView

schema_view = get_schema_view(
    openapi.Info(
        title="Where From API",
        default_version='v1',
        description="Guess a person's country of origin by name",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("names/", NameLookupView.as_view(), name="name-lookup"),
    path("popular-names/", PopularNamesView.as_view(), name="popular-names"),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
