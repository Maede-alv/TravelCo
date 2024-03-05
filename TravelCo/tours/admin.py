from django.contrib import admin
from .models import Tour, Booking, Category, Promotion, TourSchedule


class TourScheduleInline(admin.TabularInline):
    model = TourSchedule
    extra = 0


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "duration",
        "price",
        "available",
        "max_capacity",
    )
    list_filter = (
        "duration",
        "price",
        "max_capacity",
    )
    search_fields = ("title",)
    date_hierarchy = "schedules__start_time"
    list_per_page = 20
    raw_id_fields = ("category",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [TourScheduleInline]


@admin.register(TourSchedule)
class TourScheduleAdmin(admin.ModelAdmin):
    list_display = ("tour", "start_time", "end_time")
    list_filter = ("start_time", "end_time")
    search_fields = ("tour__title",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("tour", "user", "adults", "children", "babies", "paid")
    list_filter = ("paid",)
    raw_id_fields = ("tour", "user")


admin.site.register(Category)
admin.site.register(Promotion)
