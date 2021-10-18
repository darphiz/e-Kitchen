from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'))
    order_code = models.CharField(max_length=250, unique=True,blank=True,null=True)
    details = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    taken_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='taken_by')
    fulfilled_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True, related_name='fulfilled_by')
    status = models.CharField(max_length=10, null=True, blank=True,
                              choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.order_code


