from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class RegistrationSerializer(serializers.ModelSerializer):
     """
    Serializer responsible for handling user registration.
    Includes password confirmation and basic validation such as
    email uniqueness and password match.
    """
     confirmed_password = serializers.CharField(write_only=True)

     class Meta:
        """
        Meta configuration specifying the model used (User)
        and the fields that will be serialized.
        'password' is write-only for security reasons.
        """
        model = User
        fields = ['username', 'email', 'password', 'confirmed_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'email': {
                'required': True
            }
        }

     def validate_confirmed_password(self, value):
         """
        Ensure that the confirmed password matches the original password.
        If not, raise a validation error.
        """
         password = self.initial_data.get('password')
         if password and value and password != value:
            raise serializers.ValidationError('Passwords do not match')
         return value

     def validate_email(self, value):
        """
        Validate that the provided email does not already exist in the database.
        Prevents multiple accounts using the same email.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

     def save(self):
        """
        Create and save a new user instance.
        The password is hashed using Django's built-in set_password method.
        """
        pw = self.validated_data['password']

        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(pw)
        account.save()
        return account
    




User=get_user_model()
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer overriding the default behavior to manually verify
    username and password before generating JWT tokens.
    """
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)

    

    def validate(self,attrs):
        """
        Validate the provided login credentials:
        - Ensure user exists
        - Check the password manually
        - If valid, proceed with SimpleJWT token generation

        Adds the user's email to the returned attributes.
        """
        username=attrs.get("username")
        password=attrs.get("password")
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
         raise serializers.ValidationError("ungültiger Username oder Password")
        if not user.check_password(password):
            raise serializers.ValidationError("ungültiger Username oder Password")
        attrs['email']=user.email
        data=super().validate(attrs)
        return data



