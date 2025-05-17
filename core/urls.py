from django.urls import path
from .views import NameLookupView

urlpatterns = [
    path("names/", NameLookupView.as_view(), name="name-lookup"),
]
