from django.db import models
from django.contrib.auth.models import User
from django.core import validators
import datetime

# Create your models here.

# Task collection schema
class Task(models.Model):

    PRIORITY = [('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')]
    STATUS = [(True, 'Completed'), (False, 'Not Completed')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField()
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, default='Low', choices=PRIORITY)
    status = models.BooleanField(default=False, choices=STATUS)
    category = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta: 
        ordering: ['status']