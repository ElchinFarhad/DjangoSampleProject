from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()  #similar to char but with multiple line of text
    date_posted=models.DateTimeField(default=timezone.now) #auto_now_add=True, timezone.now is function but we donot put ()
                                                           # because we do not want to initalize now
    author=models.ForeignKey(User, on_delete=models.CASCADE) # if user deleted post also deleted with on_delete

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse ('post-detail', kwargs={'pk': self.pk})