from django.db import models
from django.contrib.auth.models import User
# Create your models here.

"""
The Profile model for tracking the type of user. 
it takes a foreign key of the default User model
"""

class Profile(models.Model):
    USER_CHOICES = (
        ('manager', 'Manager'),
        ('kitchen', 'Kitchen'),
        ('counter', 'Counter')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True,)
    user_type = models.CharField(max_length=10, null=True, blank=True,
                              choices=USER_CHOICES, default='counter')
    
    def __str__(self):
        return self.user.username


