from rest_framework import serializers
from phonebookapi.models import phonebook,UserToken


class  PhonebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = phonebook
        # fields = '__all__'
        fields = ('UserName', 'Password','PhoneNumber', 'last_modify_date', 'created')
        
class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToken
        # fields = '__all__'
        fields = ('user','token')
