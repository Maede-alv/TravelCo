from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self) -> str:
        return self.name


class Tour(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True, unique=True)
    image = models.ImageField(blank=True, upload_to="tour/%Y/%m/%d")
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    capacity = models.PositiveIntegerField()

    category = models.ForeignKey(
        Category, related_name="tours", on_delete=models.RESTRICT
    )
    social_sharing = models.BooleanField(default=False)

    class Meta:
        ordering = ["-available"]
        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["title"]),
            models.Index(fields=["-available"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class TourSchedule(models.Model):
    tour = models.ForeignKey(Tour, related_name="schedules",
                             on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.start_time.strftime('%b %d, %Y %H:%M')} -\
                {self.end_time.strftime('%b %d, %Y %H:%M')}"


class Booking(models.Model):
    tour = models.ForeignKey(Tour, related_name="bookings",
                             on_delete=models.PROTECT)
    user = models.ForeignKey(User, related_name="bookings",
                             on_delete=models.PROTECT)
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    babies = models.PositiveIntegerField(default=0)

    booking_date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ["booking_date"]

    def __str__(self):
        return f"{self.tour.title} - {self.user.username}"


class Promotion(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["active"]

    def __str__(self):
        return self.title
