from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=300)
    cover = models.ImageField(upload_to="covers/")
    file = models.FileField(upload_to="books/")
    file_size = models.BigIntegerField()
    format = models.CharField(max_length=10, default="fb2")
    flibusta_id = models.CharField(max_length=100, unique=True, null=True)
    added_date = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=50, default="ru")
    description = models.TextField(blank=True)
    progress_percent = models.FloatField(default=0)
    last_position = models.IntegerField(default=0)

    def __str__(self):
        return self.title
