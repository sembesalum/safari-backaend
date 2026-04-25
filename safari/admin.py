from django.contrib import admin

from .models import Booking, GalleryItem, Package, StaffProfile, Tour, TransferService


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "duration_days", "updated_at")
    list_filter = ("status",)
    search_fields = ("title", "subtitle")


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "updated_at")
    list_filter = ("status", "category")
    search_fields = ("title",)


@admin.register(TransferService)
class TransferServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "segment", "status", "updated_at")
    list_filter = ("segment", "status")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("reference_code", "guest_name", "email", "booking_type", "service_date", "status")
    list_filter = ("status", "booking_type")
    search_fields = ("reference_code", "guest_name", "email", "item_name")
    raw_id_fields = ("tour", "package", "transfer_service")


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("title", "media_type", "category", "sort_order", "updated_at")
    list_filter = ("media_type", "category")


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "status", "last_active")
    list_filter = ("role", "status")
