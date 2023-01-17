from django.test import TestCase, Client
from django.urls import reverse
from .models import *
import json
from datetime import datetime

# Create your tests here.

class TestViews(TestCase):


    def setUp(self):
        self.client = Client()
        self.starting_page = reverse('starting-page')
        self.movies_page = reverse('movies-page')
        self.movie_detail_page = reverse('movie-detail-page', args=['test-movie'])
        self.check_list = reverse('check-list')

        self.test_movie = Movie.objects.create(
        image='image',
        release_date='2023-01-16',
        slug='test-movie'
        )

    def test_collection_index_GET(self):
        res = self.client.get(self.starting_page)
        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, "collection/index.html")

    def test_collection_all_movies_GET(self):
        res = self.client.get(self.movies_page)
        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, "collection/all-movies.html")

    def test_collection_movie_detail_GET(self):
        res = self.client.get(self.movie_detail_page)
        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, "collection/movie-detail.html")

    def test_collection_check_list_GET(self):
        res = self.client.get(self.check_list)
        self.assertEquals(res.status_code, 200)
        self.assertTemplateUsed(res, "collection/check-list.html")

    def test_collection_movie_detail_comment_POST(self):
        res = self.client.post(self.movie_detail_page, {
            "user_name": "Test Name",
            "user_email": "test@email.com",
            "text": "test Comment"
        })
        self.assertEquals(res.status_code, 302)
        self.assertEquals(self.test_movie.comments.first().text, 'test Comment')
