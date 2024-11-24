from django.db import models

class Video(models.Model):
    video_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail_url = models.URLField(max_length=200)
    video_url=models.URLField(max_length=100)

    def __str__(self):
        return self.title

class Comment(models.Model):
    video_id = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    author_image_url=models.URLField(max_length=200)
    text = models.TextField()
    category = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.author}: {self.text[:30]}...'
