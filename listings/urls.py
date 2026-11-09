from rest_framework.routers import SimpleRouter

from .views import ListingViewSet

router = SimpleRouter()
router.register("listings", ListingViewSet, basename="listing")
urlpatterns = router.urls
