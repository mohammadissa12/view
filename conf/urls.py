from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI

from account.controllers import auth_controller
from place.controllers import place_controller,favorite_places_controller,review_controller,search_controller,trip_controller,merchant_controller
from location.controllers import country_controller

api = NinjaAPI()
api.add_router('auth/', auth_controller)
api.add_router('countries/', country_controller)
api.add_router('places/', place_controller)
# api.add_router('advertisements/', advertisement_controller)
# api.add_router('recommended-places/', RecommendedPlaces_controller)
# api.add_router('latest-places/', latest_places_controller)
api.add_router('favorite_places',favorite_places_controller)
api.add_router('reviews/',review_controller)
api.add_router('trips/',trip_controller)
api.add_router('search/',search_controller)
api.add_router('merchants/',merchant_controller)
from conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
