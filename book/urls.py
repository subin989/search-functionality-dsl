from django.urls import path, include
from .views import AddBookView, SearchView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"books", AddBookView, basename="book")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/search/", SearchView.as_view({"get": "list"}), name="search-view"),
]
