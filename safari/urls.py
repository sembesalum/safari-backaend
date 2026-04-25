from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

router = DefaultRouter()
router.register(r"packages", views.PackageViewSet, basename="package")
router.register(r"tours", views.TourViewSet, basename="tour")
router.register(r"transfers", views.TransferServiceViewSet, basename="transfer")
router.register(r"gallery", views.GalleryItemViewSet, basename="gallery")
router.register(r"bookings", views.BookingViewSet, basename="booking")
router.register(r"users", views.StaffUserViewSet, basename="staff-user")

urlpatterns = [
    path("health/", views.health_view),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/me/", views.me_view),
    path("auth/me/activity/", views.ping_activity_view),
    path("analytics/overview/", views.AnalyticsOverviewView.as_view()),
    path("analytics/series/", views.AnalyticsSeriesView.as_view()),
    path("team/invite/", views.StaffUserInviteView.as_view()),
    path("", include(router.urls)),
]
