from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.urls import reverse
from django.views import View

from .models import Movie
from .forms import CommentForm


# Create your views here.


class StartingPageView(ListView):
    template_name = "collection/index.html"
    model = Movie
    ordering = ["-release_date"]
    context_object_name = "movies"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset.filter(favorite=True)
        return data


class AllMoviesView(ListView):
    template_name = "collection/all-movies.html"
    model = Movie
    ordering = ["-release_date"]
    context_object_name = "all_movies"


class SingleMovieView(View):

    def is_stored_movie(self, request, movie_id):
        stored_movies = request.session.get("stored_movies")
        if stored_movies is not None:
            is_saved_for_later = movie_id in stored_movies
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self, request, slug):
        movie = Movie.objects.get(slug=slug)

        context = {
            "movie": movie,
            "movie_tags": movie.tags.all(),
            "comment_form": CommentForm(),
            "comments": movie.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_movie(request, movie.id)
        }
        return render(request, "collection/movie-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        movie = Movie.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.movie = movie
            comment.save()
            return HttpResponseRedirect(reverse("movie-detail-page", args=[slug]))

        context = {
            "movie": movie,
            "movie_tags": movie.tags.all(),
            "comment_form": comment_form,
            "saved_for_later": self.is_stored_movie(request, movie.id)
        }
        return render(request, "collection/movie-detail.html", context)


class CheckListView(View):

    def get(self, request):
        stored_movies = request.session.get("stored_movies")

        context = {}

        if stored_movies is None or len(stored_movies) == 0:
            context["movies"] = []
            context["has_movies"] = False
        else:
            posts = Movie.objects.filter(id__in=stored_movies)
            context["movies"] = posts
            context["has_movies"] = True

        return render(request, "collection/check-list.html", context)

    def post(self, request):
        stored_movies = request.session.get("stored_movies")
        if stored_movies is None:
            stored_movies = []

        movie_id = int(request.POST["movie_id"])

        if movie_id not in stored_movies:
            stored_movies.append(movie_id)
        else:
            stored_movies.remove(movie_id)
        request.session["stored_movies"] = stored_movies

        return HttpResponseRedirect("/")
