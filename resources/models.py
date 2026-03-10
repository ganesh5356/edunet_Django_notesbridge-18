from django.db import models
from django.contrib.auth.models import User


class Resource(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField()

    department = models.CharField(max_length=100)

    semester = models.IntegerField()

    subject = models.CharField(max_length=100)

    resource_type = models.CharField(max_length=50)

    file = models.FileField(upload_to='resources/')

    uploaded_by = models.ForeignKey(User,on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Bookmark(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    resource = models.ForeignKey(Resource,on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bookmarked {self.resource.title}"