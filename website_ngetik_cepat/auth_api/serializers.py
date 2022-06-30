from tokenize import Token
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        # token['name'] = f'{user.first_name} {user.last_name}'
        token['username'] = user.username
        return token
        


# class RegisterSerializer(serializers.ModelSerializer):

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            print("password is validated")
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )
        
        user.set_password(validated_data['password'])
        print(validated_data)
        user.save()

        return user


class RegisterSerializer(serializers.ModelSerializer):
    #buat memvalidasi data yang dikirim dari client ke server, udah cocok belum sama yang dibuat di bawah 
    # email = serializers.EmailField(
    #         required=False,
    #         validators=[UniqueValidator(queryset=User.objects.all())]
    #         )
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    #sampai sini

    class Meta:
        model = User
        # Fields field shows which fields from the Model class to show in your new Form.
        fields = ('username', 'password', )

    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError({"password": "Password fields didn't match."})

    #     return attrs

    def create(self, validated_data):
        # data yang mau dimasukin ke database user
        user = User.objects.create(
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user