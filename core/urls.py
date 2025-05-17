from django.urls import path
from .views import NameLookupView, PopularNamesView

urlpatterns = [
    path("names/", NameLookupView.as_view(), name="name-lookup"),
    path("popular-names/", PopularNamesView.as_view(), name="popular-names"),
]
