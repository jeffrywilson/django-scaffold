from django.contrib.auth import get_user_model

from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from dj_rest_auth.serializers import PasswordResetSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer

# Basic model serializer for users
class UserSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source="__str__")

    class Meta:
        model = get_user_model()
        fields = ('id', 'name', 'photo')


#Detail Serializers
class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', 'phone')


class UserRegisterSerializer(RegisterSerializer):
    phone = PhoneNumberField(required=False)

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['phone'] = self.validated_data.get('phone', None)
        return data_dict



class UserPasswordResetSerializer(PasswordResetSerializer):

    def validate_email(self, value):
        User = get_user_model()
        value = super(UserPasswordResetSerializer, self).validate_email(value)
        if not User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError({
                "error": "Email does not exist"
            })
        return value
