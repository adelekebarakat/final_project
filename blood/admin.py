from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Emergency, BloodType, CanDonateTo, CanReceiveFrom, ReasonForRequest

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username','get_blood_type','phone_number', 'email')

    def get_blood_type(self, obj):
        return obj.blood_type  # Access blood type through the ForeignKey relationship

    get_blood_type.short_description = 'Blood Type'


class EmergencyAdmin(admin.ModelAdmin):
    list_display = ('get_blood_type', 'reason_for_request', 'location', 'contact_number')


    def get_blood_type(self, obj):
        return obj.blood_type  # Access blood type through the ForeignKey relationship


admin.site.register(User, UserAdmin)
admin.site.register(BloodType)
admin.site.register(CanDonateTo)
admin.site.register(CanReceiveFrom)
admin.site.register(Emergency, EmergencyAdmin)
admin.site.register(ReasonForRequest)
