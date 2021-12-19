from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    user_type = models.CharField(max_length=20, choices=(('client', 'cliente'), ('professional', 'profesional')), default='cliente')

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username

class Offer(models.Model):
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, default='Active')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    days = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.title

class Messages(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    update_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message