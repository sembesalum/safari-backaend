from django.contrib.auth import get_user_model
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, GalleryItem, Package, StaffProfile, Tour, TransferService
from .permissions import IsStaffUser
from .serializers import (
    BookingSerializer,
    GalleryItemSerializer,
    PackageSerializer,
    StaffUserSerializer,
    TourSerializer,
    TransferServiceSerializer,
    UserInviteSerializer,
)

User = get_user_model()


def _public_active_qs(model, manager="objects"):
    """For list: anonymous users only see active/public content."""
    qs = getattr(model, manager).all()
    if hasattr(model, "status"):
        if model == Package:
            return qs.filter(status=Package.Status.ACTIVE)
        if model == Tour:
            return qs.filter(status=Tour.Status.ACTIVE)
        if model == TransferService:
            return qs.filter(status=TransferService.Status.ACTIVE)
    return qs


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsStaffUser()]

    def get_queryset(self):
        qs = Package.objects.all().order_by("-updated_at")
        if self.action == "list" and not self.request.user.is_authenticated:
            return qs.filter(status=Package.Status.ACTIVE)
        return qs


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsStaffUser()]

    def get_queryset(self):
        qs = Tour.objects.all().order_by("-updated_at")
        if self.action == "list" and not self.request.user.is_authenticated:
            return qs.filter(status=Tour.Status.ACTIVE)
        return qs


class TransferServiceViewSet(viewsets.ModelViewSet):
    queryset = TransferService.objects.all()
    serializer_class = TransferServiceSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsStaffUser()]

    def get_queryset(self):
        qs = TransferService.objects.all().order_by("segment", "-updated_at")
        if self.action == "list" and not self.request.user.is_authenticated:
            return qs.filter(status=TransferService.Status.ACTIVE)
        return qs


class GalleryItemViewSet(viewsets.ModelViewSet):
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsStaffUser()]

    def get_queryset(self):
        return GalleryItem.objects.all().order_by("sort_order", "-updated_at")


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated(), IsStaffUser()]

    def get_queryset(self):
        return Booking.objects.all().select_related("tour", "package", "transfer_service").order_by(
            "-created_at"
        )


class StaffUserViewSet(viewsets.ReadOnlyModelViewSet):
    """Team & access — staff users with profile."""

    serializer_class = StaffUserSerializer
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get_queryset(self):
        return (
            User.objects.filter(Q(is_staff=True) | Q(staff_profile__isnull=False))
            .select_related("staff_profile")
            .order_by("email")
        )


class StaffUserInviteView(APIView):
    permission_classes = [IsAuthenticated, IsStaffUser]

    def post(self, request):
        ser = UserInviteSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        email = ser.validated_data["email"].lower()
        name = ser.validated_data["name"].strip()
        role = ser.validated_data["role"]
        privileges = ser.validated_data.get("privileges") or []
        parts = name.split(" ", 1)
        first = parts[0]
        last = parts[1] if len(parts) > 1 else ""
        if User.objects.filter(email__iexact=email).exists():
            return Response({"detail": "User with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=first,
            last_name=last,
            is_active=False,
        )
        user.set_unusable_password()
        user.save()
        StaffProfile.objects.create(user=user, role=role, privileges=privileges, status=StaffProfile.Status.INVITED)
        return Response(StaffUserSerializer(user).data, status=status.HTTP_201_CREATED)


class AnalyticsOverviewView(APIView):
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get(self, request):
        now = timezone.now()
        start_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        bookings_month = Booking.objects.filter(created_at__gte=start_month).count()
        pending = Booking.objects.filter(status=Booking.Status.NEW).count()
        revenue_agg = Booking.objects.filter(created_at__gte=start_month).aggregate(
            total=Sum("estimated_revenue")
        )
        total = revenue_agg["total"]
        revenue_month = f"TSh {int(total):,}" if total is not None else "TSh 0"
        active_packages = Package.objects.filter(status=Package.Status.ACTIVE).count()
        active_tours = Tour.objects.filter(status=Tour.Status.ACTIVE).count()
        return Response(
            {
                "bookingsMonth": bookings_month,
                "revenueMonth": revenue_month,
                "pendingBookings": pending,
                "activePackages": active_packages,
                "activeTours": active_tours,
            }
        )


class AnalyticsSeriesView(APIView):
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get(self, request):
        """Monthly booking counts + revenue sum (last 12 months)."""
        from dateutil.relativedelta import relativedelta

        now = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        since = now - relativedelta(months=11)

        rows = (
            Booking.objects.filter(created_at__gte=since)
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(bookings=Count("id"), revenue=Sum("estimated_revenue"))
            .order_by("month")
        )
        out = []
        for r in rows:
            m = r["month"]
            label = m.strftime("%b") if m else ""
            rev = r["revenue"] or 0
            out.append(
                {
                    "label": label,
                    "bookings": r["bookings"],
                    "revenue": int(rev) if rev else 0,
                }
            )
        return Response(out)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    user = request.user
    data = {
        "id": user.pk,
        "email": user.email,
        "username": user.username,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "isStaff": user.is_staff,
    }
    if hasattr(user, "staff_profile"):
        p = user.staff_profile
        data["role"] = p.role
        data["privileges"] = p.privileges
        data["staffStatus"] = p.status
    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsStaffUser])
def ping_activity_view(request):
    if hasattr(request.user, "staff_profile"):
        request.user.staff_profile.last_active = timezone.now()
        request.user.staff_profile.save(update_fields=["last_active"])
    return Response({"ok": True})


@api_view(["GET"])
@permission_classes([AllowAny])
def health_view(request):
    return Response({"status": "ok", "service": "safari-island-api"})
