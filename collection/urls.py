from django.urls import path
from . import views

urlpatterns = [
    path("", views.StartingPageView.as_view(), name="starting-page"),
    path("movies", views.AllMoviesView.as_view(), name="movies-page"),
    path("movies/<slug:slug>", views.SingleMovieView.as_view(), name="movie-detail-page"), # noqa
    path("check-list", views.CheckListView.as_view(), name="check-list")
]
