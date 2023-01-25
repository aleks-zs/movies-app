from django.test import TestCase
from collection.models import Tag, Director, Movie, Comment


class ModelsTests(TestCase):

    def test_create_tag(self):
        tag = Tag.objects.create(caption='tag')
        self.assertEqual(str(tag), tag.caption)

    def test_create_director(self):
        director = Director.objects.create(first_name='a', last_name='z')
        self.assertEqual(str(director), director.fullname())

    def test_create_movie(self):
        image = 'image'
        release_date = '2023-01-25'
        slug = 'slug'
        movie = Movie.objects.create(
            title='title',
            image=image,
            release_date=release_date,
            slug=slug
        )

        self.assertEqual(str(movie), movie.title)
        self.assertEqual(movie.image, image)
        self.assertEqual(movie.release_date, release_date)
        self.assertEqual(movie.slug, slug)

    def test_create_comment(self):
        user_name = 'username'
        user_email = 'user@email.com'
        text = 'text'
        movie = Movie.objects.create(
            title='title',
            image='image',
            release_date='2023-01-25',
            slug='slug'
        )

        comment = Comment.objects.create(
            user_name=user_name,
            user_email=user_email,
            text=text,
            movie=movie
        )

        self.assertEqual(comment.user_name, user_name)
        self.assertEqual(comment.user_email, user_email)
        self.assertEqual(comment.text, text)
        self.assertEqual(comment.movie, movie)
