import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class Package(models.Model):
    """Full CMS package — matches marketing Packages page + dashboard."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        DRAFT = "draft", "Draft"
        ARCHIVED = "archived", "Archived"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(
        max_length=280, unique=True, null=True, blank=True, help_text="URL segment; auto from title if unset"
    )
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True, help_text="Long intro / marketing copy (desc on site)")
    duration_days = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    base_price = models.CharField(
        max_length=255,
        blank=True,
        help_text="Short headline price for cards e.g. TSh 1,196,000 per person (6+)",
    )
    highlights = models.JSONField(default=list, blank=True, help_text='["bullet", ...]')
    itinerary = models.JSONField(default=list, blank=True, help_text='["Day 1: ...", ...]')
    # Either use flat prices OR grouped tables (same as frontend)
    prices = models.JSONField(
        default=list,
        blank=True,
        help_text='[{"people": "1 Person", "price": "$100"}, ...] when not using price_groups',
    )
    price_groups = models.JSONField(
        default=list,
        blank=True,
        help_text='[{"title": "Best Value", "rows": [{"people": "...", "price": "..."}]}]',
    )
    special_offers = models.JSONField(default=list, blank=True, help_text='["offer line", ...]')
    important_info = models.JSONField(default=list, blank=True, help_text='["note", ...]')
    hero_image = models.ImageField(upload_to="packages/", blank=True, null=True)
    hero_image_url = models.URLField(max_length=2000, blank=True, help_text="If set, can be used instead of upload")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated_at"]

    def save(self, *args, **kwargs):
        if self.slug in (None, "") and self.title:
            from django.utils.text import slugify

            base = slugify(self.title)[:250] or "package"
            slug = base
            n = 0
            while Package.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f"{base}-{n}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tour(models.Model):
    """Full CMS day tour — matches marketing Tours page + dashboard."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        DRAFT = "draft", "Draft"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=280, unique=True, null=True, blank=True)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=120)
    description = models.TextField(blank=True, help_text="Main paragraph (desc)")
    includes = models.TextField(blank=True, help_text="Comma-separated style sentence or bullet line")
    highlights = models.JSONField(default=list, blank=True, help_text='["bullet", ...]')
    bonuses = models.JSONField(default=list, blank=True, help_text='["bonus perk", ...] optional')
    prices = models.JSONField(
        default=list,
        blank=True,
        help_text='[{"people": "1 Person", "price": "$50"}, ...]',
    )
    from_price = models.CharField(max_length=255, blank=True, help_text="Headline ‘from’ for listings")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    hero_image = models.ImageField(upload_to="tours/", blank=True, null=True)
    hero_image_url = models.URLField(max_length=2000, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated_at"]

    def save(self, *args, **kwargs):
        if self.slug in (None, "") and self.title:
            from django.utils.text import slugify

            base = slugify(self.title)[:250] or "tour"
            slug = base
            n = 0
            while Tour.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f"{base}-{n}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class TransferService(models.Model):
    """Transfer product row + optional structured pricing for airport/half/full pages."""

    class Segment(models.TextChoices):
        AIRPORT = "airport", "Airport & hotel"
        HALF_DAY = "half_day", "Half day"
        FULL_DAY = "full_day", "Full day"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        DRAFT = "draft", "Draft"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=280, unique=True, null=True, blank=True)
    title = models.CharField(max_length=255)
    segment = models.CharField(max_length=20, choices=Segment.choices)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True, help_text="Extra HTML-free copy for apps")
    from_price = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    # Flexible payloads for UI: airport routes, tier grids, includes/excludes, etc.
    pricing_payload = models.JSONField(
        default=dict,
        blank=True,
        help_text="e.g. airport_routes, half_day_tiers, full_day_tiers, includes, excludes, notes",
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["segment", "-updated_at"]

    def save(self, *args, **kwargs):
        if self.slug in (None, "") and self.title:
            from django.utils.text import slugify

            base = slugify(self.title)[:250] or "transfer"
            slug = base
            n = 0
            while TransferService.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f"{base}-{n}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Booking(models.Model):
    """Inquiry / booking — tour & package form + transfer forms (airport / half / full day)."""

    class BookingType(models.TextChoices):
        TOUR = "tour", "Tour"
        PACKAGE = "package", "Package"
        TRANSFER = "transfer", "Transfer"

    class Status(models.TextChoices):
        NEW = "new", "New"
        CONFIRMED = "confirmed", "Confirmed"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    class TransferSegment(models.TextChoices):
        AIRPORT = "airport", "Airport & hotel"
        HALF_DAY = "half_day", "Half day"
        FULL_DAY = "full_day", "Full day"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference_code = models.CharField(max_length=32, unique=True, editable=False)

    # Contact (Create Your Tour / generic)
    guest_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=64, blank=True)
    country = models.CharField(max_length=120, blank=True)

    booking_type = models.CharField(max_length=20, choices=BookingType.choices)
    item_name = models.CharField(max_length=500, blank=True, help_text="Primary label / package title / transfer summary")

    tour = models.ForeignKey(Tour, null=True, blank=True, on_delete=models.SET_NULL, related_name="bookings")
    package = models.ForeignKey(Package, null=True, blank=True, on_delete=models.SET_NULL, related_name="bookings")
    transfer_service = models.ForeignKey(
        TransferService, null=True, blank=True, on_delete=models.SET_NULL, related_name="bookings"
    )

    # Party & schedule
    adults = models.PositiveSmallIntegerField(null=True, blank=True)
    children = models.PositiveSmallIntegerField(null=True, blank=True)
    party_size = models.PositiveIntegerField(default=1, help_text="Total pax if not splitting adults/children")
    service_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)

    hotel = models.CharField(max_length=255, blank=True)
    room = models.CharField(max_length=64, blank=True)
    language = models.CharField(max_length=64, blank=True)

    # Tour/package multi-select & extras (Create Your Adventure form)
    selected_tours = models.JSONField(default=list, blank=True, help_text="List of tour names when booking_type=tour")
    selected_package_name = models.CharField(max_length=500, blank=True, help_text="Chosen package title if no FK")
    transport_needed = models.CharField(max_length=8, blank=True, help_text="Yes / No")
    pickup_location = models.CharField(max_length=500, blank=True)
    dropoff_location = models.CharField(max_length=500, blank=True)
    additional_services = models.JSONField(default=list, blank=True, help_text='["Drone & photographer", ...]')
    comment = models.TextField(blank=True)
    special_requests = models.TextField(blank=True)

    # Transfer-specific (nullable when not transfer)
    transfer_segment = models.CharField(
        max_length=20, choices=TransferSegment.choices, blank=True, help_text="Which transfer form"
    )
    suitcases = models.PositiveSmallIntegerField(null=True, blank=True)
    pickup_time_note = models.CharField(max_length=255, blank=True, help_text="Free text pickup time")
    flight_number = models.CharField(max_length=64, blank=True)
    transfer_direction = models.CharField(
        max_length=64, blank=True, help_text="e.g. Airport to hotel / Hotel to airport"
    )
    tour_destination = models.CharField(max_length=500, blank=True)
    preferred_datetime = models.CharField(max_length=255, blank=True, help_text="Half day: date + time")
    custom_destination_request = models.TextField(blank=True)
    transfer_time_note = models.CharField(max_length=255, blank=True, help_text="Full day: start window")
    customize_destination_request = models.TextField(blank=True)
    pricing_selection = models.JSONField(
        null=True,
        blank=True,
        help_text="Snapshot from site: route, tier, price lines for WhatsApp parity",
    )

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    notes = models.TextField(blank=True, help_text="Internal staff notes")
    estimated_revenue = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.reference_code:
            self.reference_code = self._generate_reference()
        super().save(*args, **kwargs)

    @staticmethod
    def _generate_reference():
        return f"BK-{timezone.now().strftime('%y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    def __str__(self):
        return f"{self.reference_code} — {self.guest_name}"


class GalleryItem(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = "image", "Image"
        VIDEO = "video", "Video"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    media_type = models.CharField(max_length=10, choices=MediaType.choices)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=120)
    sort_order = models.PositiveIntegerField(default=0)
    src = models.URLField(max_length=2000, blank=True, help_text="Public URL for image")
    image = models.ImageField(upload_to="gallery/images/", blank=True, null=True)
    youtube_id = models.CharField(max_length=32, blank=True)
    file_src = models.URLField(max_length=2000, blank=True, help_text="Direct MP4/stream URL or absolute path")
    video = models.FileField(upload_to="gallery/videos/", blank=True, null=True)
    poster_src = models.URLField(max_length=2000, blank=True)
    poster = models.ImageField(upload_to="gallery/posters/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "-updated_at"]

    def __str__(self):
        return f"{self.title} ({self.media_type})"


class StaffProfile(models.Model):
    class Role(models.TextChoices):
        SUPER_ADMIN = "super_admin", "Super admin"
        ADMIN = "admin", "Admin"
        EDITOR = "editor", "Editor"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INVITED = "invited", "Invited"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="staff_profile")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.EDITOR)
    privileges = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    last_active = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} ({self.role})"
