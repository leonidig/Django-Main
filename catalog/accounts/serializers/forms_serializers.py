from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterFormSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    captcha = serializers.CharField(required=True)

    # class Meta:
    #     model = User
    #     extra_fields = ["email"]
    #     fields = ["username", "password1", "password2"]



class CaptchaFieldSerializer(serializers.Serializer):
    captcha_0 = serializers.CharField(required=True)
    captcha_1 = serializers.CharField(required=True)
    
    def validate(self, attrs):
        from captcha.models import CaptchaStore
        
        try:
            captcha = CaptchaStore.objects.get(hashkey=attrs["captcha_0"])
            
        except CaptchaStore.DoesNotExist:
            raise serializers.ValidationError('Incorrect Captcha')
        
        if captcha.response != attrs.get('captcha_1', '').lower():
            raise serializers.ValidationError('Invalid captcha')
        
        captcha.delete()
        return attrs 