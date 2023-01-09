from django.db import models
from django.core.validators import MinLengthValidator


# Create your models here.


class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.caption}"


class Director(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    title = models.CharField(max_length=150)
    excerpt = models.CharField(max_length=200)
    image = models.ImageField(upload_to="movies", null=True)
    release_date = models.DateField()
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True, related_name='movies')
    tags = models.ManyToManyField(Tag)
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")
