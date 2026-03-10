from django.db import models
from django.contrib.auth.models import User


class Resource(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
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


class Doubt(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    question = models.TextField()
    asked_by = models.CharField(max_length=100)
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.asked_by}"


class Download(models.Model):
    resource_id = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} downloaded {self.resource_id}"