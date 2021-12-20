from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(AbstractUser):

    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(unique=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    user_type = models.CharField(max_length=20, choices=(('client', 'cliente'), ('professional', 'profesional')), default='cliente')
    avatar = models.ImageField(null=True, default="avatar.svg")
    #district = models.CharField(max_length=100, blank=True)
    #province = models.CharField(max_length=100, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def is_professional(self):
        return self.user_type == 'professional'

    def __str__(self):
        return self.email

class Offer(models.Model):
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    aspirant = models.ManyToManyField(User, related_name='aspirant', blank=True)    
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=(('active', 'activo'), ('processing', 'proceso'), ('finished', 'finalizado')), default='activo')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    days = models.IntegerField()
    #district = models.CharField(max_length=100, blank=True)
    #province = models.CharField(max_length=100, blank=True)

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
        return self.content