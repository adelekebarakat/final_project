from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class BloodType(models.Model):
    blood_type = models.CharField(max_length=4)
    def __str__(self):
        return self.blood_type


class User(AbstractUser):
    phone_number = models.CharField(max_length=22, blank=True, null=True)
    blood_type = models.ForeignKey(BloodType, on_delete=models.SET_NULL, blank=True, null=True)

class ReasonForRequest(models.Model):
    reason = models.CharField(max_length=225, null=True, blank=True)


    def __str__(self):
        return self.reason


class Emergency(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    blood_type = models.ForeignKey(BloodType, on_delete=models.SET_NULL, blank=True, null=True)
    # reason_for_request = models.TextField()
    reason_for_request = models.ForeignKey(ReasonForRequest, on_delete=models.SET_NULL, blank=True, null=True)
    location = models.TextField()
    contact_number = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return f'Emergency Request by {self.user.username} for {self.blood_type}'




class CanDonateTo(models.Model):
    blood_type = models.ForeignKey(BloodType, related_name='can_donate_to', on_delete=models.SET_NULL, blank=True, null=True)
    can_donate_to = models.ForeignKey(BloodType, on_delete=models.SET_NULL, related_name='+',  blank=True, null=True)

    class Meta:
        unique_together = ('blood_type', 'can_donate_to')
    
    def __str__(self):
        return f'{self.blood_type} can donate to {self.can_donate_to}'

class CanReceiveFrom(models.Model):
    blood_type = models.ForeignKey(BloodType, related_name='can_receive_from', on_delete=models.SET_NULL, blank=True, null=True)
    can_receive_from = models.ForeignKey(BloodType, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        unique_together = ('blood_type', 'can_receive_from')
    
    def __str__(self):
        return f'{self.blood_type} can receive from{self.can_receive_from}'


    