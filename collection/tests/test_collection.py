from django.test import TestCase, Client
from django.urls import reverse
from collection.models import Movie

# Create your tests here.


def create_movie(image, release_date, slug):
    return Movie.objects.create(
        image=image,
        release_date=release_date,
        slug=slug
    )


class ViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.starting_page = reverse('starting-page')
        self.movies_page = reverse('movies-page')
        self.movie_detail_page = reverse('movie-detail-page', args=['stored-movie']) # noqa
        self.check_list = reverse('check-list')

    def test_get_collection_index(self):
        res = self.client.get(self.starting_page)
        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, "collection/index.html")

    def test_get_collection_all_movies(self):
        res = self.client.get(self.movies_page)
        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, "collection/all-movies.html")

    def test_get_collection_movie_detail(self):
        create_movie('image', '2023-01-25', 'stored-movie')
        res = self.client.get(self.movie_detail_page)
        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, "collection/movie-detail.html")

    def test_get_collection_check_list(self):
        res = self.client.get(self.check_list)
        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, "collection/check-list.html")

    def test_post_collection_movie_detail_comment(self):
        stored_movie = create_movie('image', '2023-01-25', 'stored-movie')
        payload = {
            "user_name": "Test Name",
            "user_email": "test@email.com",
            "text": "test Comment"
        }
        res = self.client.post(self.movie_detail_page, payload)
        self.assertEquals(res.status_code, 302)
        self.assertEquals(stored_movie.comments.first().text, 'test Comment')
