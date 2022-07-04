from dataclasses import field, fields
from rest_framework import serializers
from .models import Test, UserTestResults, UsersScores, WordsSimMatrix

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = (
            'id',
            'title',
            'description', 
            'published'
        )

class UserScoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersScores
        fields = ('user_id', 'item_id', 'rating', 'word', 'sd', 'timestamp',)

class UserTestResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTestResults
        fields = '__all__'

class WordsSimMatrixSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordsSimMatrix
        fields = ('item_id', 'word', 'matrix')
