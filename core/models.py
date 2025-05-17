from django.db import models


class Country(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    official_name = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    subregion = models.CharField(max_length=255, null=True, blank=True)
    independent = models.BooleanField(null=True, blank=True)
    google_maps = models.URLField(null=True, blank=True)
    openstreetmap = models.URLField(null=True, blank=True)
    capital_name = models.CharField(max_length=255, null=True, blank=True)
    capital_lat = models.FloatField(null=True, blank=True)
    capital_lng = models.FloatField(null=True, blank=True)
    flag_png = models.URLField(null=True, blank=True)
    flag_svg = models.URLField(null=True, blank=True)
    flag_alt = models.CharField(max_length=255, null=True, blank=True)
    coat_png = models.URLField(null=True, blank=True)
    coat_svg = models.URLField(null=True, blank=True)
    borders = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.code}-{self.name}"


class Name(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, related_name="names", on_delete=models.CASCADE)
    probability = models.FloatField()
    request_count = models.PositiveIntegerField(default=1)
    last_accessed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("name", "country")

    def __str__(self):
        return f"{self.name} → {self.country.code} ({self.probability})"
