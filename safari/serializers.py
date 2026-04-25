from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Booking, GalleryItem, Package, StaffProfile, Tour, TransferService

User = get_user_model()


def _absolute_media_url(request, file_field):
    if file_field and hasattr(file_field, "url"):
        if request:
            return request.build_absolute_uri(file_field.url)
        return file_field.url
    return None


class PackageSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    slug = serializers.SlugField(required=False, allow_null=True)
    basePrice = serializers.CharField(source="base_price", required=False, allow_blank=True)
    durationDays = serializers.IntegerField(source="duration_days", required=False, default=1)
    desc = serializers.CharField(source="description", required=False, allow_blank=True)
    specialOffer = serializers.JSONField(source="special_offers", required=False)
    importantInfo = serializers.JSONField(source="important_info", required=False)
    priceGroups = serializers.JSONField(source="price_groups", required=False)
    heroImage = serializers.ImageField(source="hero_image", required=False, allow_null=True)
    heroImageUrl = serializers.URLField(source="hero_image_url", max_length=2000, required=False, allow_blank=True)
    updatedAt = serializers.DateTimeField(source="updated_at", format="%Y-%m-%d", read_only=True)
    img = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Package
        fields = [
            "id",
            "slug",
            "title",
            "subtitle",
            "desc",
            "durationDays",
            "status",
            "basePrice",
            "highlights",
            "itinerary",
            "prices",
            "priceGroups",
            "specialOffer",
            "importantInfo",
            "heroImage",
            "heroImageUrl",
            "img",
            "updatedAt",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def get_img(self, obj):
        request = self.context.get("request")
        return _absolute_media_url(request, obj.hero_image) or (obj.hero_image_url or "")


class TourSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    slug = serializers.SlugField(required=False, allow_null=True)
    fromPrice = serializers.CharField(source="from_price", required=False, allow_blank=True)
    desc = serializers.CharField(source="description", required=False, allow_blank=True)
    heroImage = serializers.ImageField(source="hero_image", required=False, allow_null=True)
    heroImageUrl = serializers.URLField(source="hero_image_url", max_length=2000, required=False, allow_blank=True)
    updatedAt = serializers.DateTimeField(source="updated_at", format="%Y-%m-%d", read_only=True)
    img = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tour
        fields = [
            "id",
            "slug",
            "title",
            "category",
            "desc",
            "includes",
            "highlights",
            "bonuses",
            "prices",
            "fromPrice",
            "status",
            "heroImage",
            "heroImageUrl",
            "img",
            "updatedAt",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def get_img(self, obj):
        request = self.context.get("request")
        return _absolute_media_url(request, obj.hero_image) or (obj.hero_image_url or "")


class TransferServiceSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    slug = serializers.SlugField(required=False, allow_null=True)
    fromPrice = serializers.CharField(source="from_price", required=False, allow_blank=True)
    desc = serializers.CharField(source="description", required=False, allow_blank=True)
    pricingPayload = serializers.JSONField(source="pricing_payload", required=False)
    updatedAt = serializers.DateTimeField(source="updated_at", format="%Y-%m-%d", read_only=True)

    class Meta:
        model = TransferService
        fields = [
            "id",
            "slug",
            "title",
            "segment",
            "summary",
            "desc",
            "fromPrice",
            "pricingPayload",
            "status",
            "updatedAt",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class BookingSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    referenceCode = serializers.CharField(source="reference_code", read_only=True)
    guestName = serializers.CharField(source="guest_name")
    bookingType = serializers.CharField(source="booking_type")
    itemName = serializers.CharField(source="item_name", required=False, allow_blank=True)
    serviceDate = serializers.DateField(source="service_date", format="%Y-%m-%d", required=False, allow_null=True)
    partySize = serializers.IntegerField(source="party_size", required=False)
    startTime = serializers.TimeField(source="start_time", required=False, allow_null=True)
    tour = serializers.PrimaryKeyRelatedField(queryset=Tour.objects.all(), allow_null=True, required=False)
    package = serializers.PrimaryKeyRelatedField(queryset=Package.objects.all(), allow_null=True, required=False)
    transferService = serializers.PrimaryKeyRelatedField(
        source="transfer_service", queryset=TransferService.objects.all(), allow_null=True, required=False
    )
    selectedTours = serializers.JSONField(source="selected_tours", required=False)
    selectedPackageName = serializers.CharField(source="selected_package_name", required=False, allow_blank=True)
    transportNeeded = serializers.CharField(source="transport_needed", required=False, allow_blank=True)
    pickupLocation = serializers.CharField(source="pickup_location", required=False, allow_blank=True)
    dropoffLocation = serializers.CharField(source="dropoff_location", required=False, allow_blank=True)
    additionalServices = serializers.JSONField(required=False)
    specialRequests = serializers.CharField(source="special_requests", required=False, allow_blank=True)
    transferSegment = serializers.CharField(source="transfer_segment", required=False, allow_blank=True)
    pickupTimeNote = serializers.CharField(source="pickup_time_note", required=False, allow_blank=True)
    flightNumber = serializers.CharField(source="flight_number", required=False, allow_blank=True)
    transferDirection = serializers.CharField(source="transfer_direction", required=False, allow_blank=True)
    tourDestination = serializers.CharField(source="tour_destination", required=False, allow_blank=True)
    preferredDatetime = serializers.CharField(source="preferred_datetime", required=False, allow_blank=True)
    customDestinationRequest = serializers.CharField(source="custom_destination_request", required=False, allow_blank=True)
    transferTimeNote = serializers.CharField(source="transfer_time_note", required=False, allow_blank=True)
    customizeDestinationRequest = serializers.CharField(source="customize_destination_request", required=False, allow_blank=True)
    pricingSelection = serializers.JSONField(source="pricing_selection", required=False, allow_null=True)
    estimatedRevenue = serializers.DecimalField(
        source="estimated_revenue", max_digits=14, decimal_places=2, allow_null=True, required=False
    )

    class Meta:
        model = Booking
        fields = [
            "id",
            "referenceCode",
            "guestName",
            "email",
            "phone",
            "country",
            "bookingType",
            "itemName",
            "tour",
            "package",
            "transferService",
            "adults",
            "children",
            "partySize",
            "serviceDate",
            "startTime",
            "hotel",
            "room",
            "language",
            "selectedTours",
            "selectedPackageName",
            "transportNeeded",
            "pickupLocation",
            "dropoffLocation",
            "additionalServices",
            "comment",
            "specialRequests",
            "transferSegment",
            "suitcases",
            "pickupTimeNote",
            "flightNumber",
            "transferDirection",
            "tourDestination",
            "preferredDatetime",
            "customDestinationRequest",
            "transferTimeNote",
            "customizeDestinationRequest",
            "pricingSelection",
            "status",
            "notes",
            "estimatedRevenue",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["reference_code", "created_at", "updated_at"]


class GalleryItemSerializer(serializers.ModelSerializer):
    """Read/write for gallery; GET JSON matches public site + dashboard shape."""

    id = serializers.UUIDField(read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", format="%Y-%m-%d", read_only=True)

    class Meta:
        model = GalleryItem
        fields = [
            "id",
            "media_type",
            "title",
            "category",
            "sort_order",
            "src",
            "image",
            "youtube_id",
            "file_src",
            "video",
            "poster_src",
            "poster",
            "updatedAt",
            "created_at",
        ]
        read_only_fields = ["created_at"]

    def to_representation(self, instance):
        request = self.context.get("request")
        common = {
            "id": str(instance.id),
            "title": instance.title,
            "category": instance.category,
            "updatedAt": instance.updated_at.strftime("%Y-%m-%d"),
        }
        if instance.media_type == GalleryItem.MediaType.IMAGE:
            url = _absolute_media_url(request, instance.image) or instance.src or ""
            return {
                **common,
                "type": "image",
                "src": url,
            }
        out = {
            **common,
            "type": "video",
            "youtubeId": instance.youtube_id or None,
            "fileSrc": _absolute_media_url(request, instance.video) or instance.file_src or None,
            "posterSrc": _absolute_media_url(request, instance.poster) or instance.poster_src or None,
        }
        return out

    def to_internal_value(self, data):
        if hasattr(data, "copy"):
            data = data.copy()
        mutable = dict(data)
        if "type" in mutable and "media_type" not in mutable:
            mutable["media_type"] = mutable.pop("type")
        if "youtubeId" in mutable:
            mutable["youtube_id"] = mutable.pop("youtubeId")
        return super().to_internal_value(mutable)

    def validate(self, attrs):
        inst = self.instance
        mt = attrs.get("media_type") or (inst and inst.media_type)
        if not mt:
            raise serializers.ValidationError({"type": "Provide `type` (image|video) or `media_type`."})
        if mt == GalleryItem.MediaType.IMAGE:
            src = attrs.get("src")
            if src is None and inst:
                src = inst.src
            img = attrs.get("image")
            has_img = bool(img) or (inst and inst.image)
            if not (src or has_img):
                raise serializers.ValidationError("Image items require `src` and/or `image` upload.")
        elif mt == GalleryItem.MediaType.VIDEO:
            y = attrs.get("youtube_id")
            fs = attrs.get("file_src")
            vid = attrs.get("video")
            if inst:
                if y is None:
                    y = inst.youtube_id
                if fs is None:
                    fs = inst.file_src
                if vid is None:
                    vid = inst.video
            if not (y or fs or vid):
                raise serializers.ValidationError("Video items require `youtube_id`, `file_src`, or `video` upload.")
        return attrs

    def create(self, validated_data):
        return GalleryItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance


class StaffUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="pk", read_only=True)
    name = serializers.SerializerMethodField()
    email = serializers.EmailField(read_only=True)
    role = serializers.SerializerMethodField()
    privileges = serializers.SerializerMethodField()
    lastActive = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "name", "email", "role", "privileges", "lastActive", "status", "is_active"]
        read_only_fields = fields

    def get_name(self, obj):
        fn = (obj.first_name or "").strip()
        ln = (obj.last_name or "").strip()
        if fn or ln:
            return f"{fn} {ln}".strip()
        return obj.username

    def get_role(self, obj):
        p = getattr(obj, "staff_profile", None)
        if p:
            return p.role
        return "super_admin" if obj.is_superuser else "admin" if obj.is_staff else None

    def get_privileges(self, obj):
        p = getattr(obj, "staff_profile", None)
        if p:
            return p.privileges
        return ["Full access"] if obj.is_superuser else []

    def get_status(self, obj):
        p = getattr(obj, "staff_profile", None)
        if p:
            return p.status
        return StaffProfile.Status.ACTIVE

    def get_lastActive(self, obj):
        p = getattr(obj, "staff_profile", None)
        if not p or not p.last_active:
            return "—"
        return p.last_active.strftime("%Y-%m-%d %H:%M UTC")


class UserInviteSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=255)
    role = serializers.ChoiceField(choices=StaffProfile.Role.choices)
    privileges = serializers.ListField(child=serializers.CharField(), required=False, default=list)
