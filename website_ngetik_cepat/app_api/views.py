from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .utils import pickRandValues, recommend_words_based_collaborative, recommend_words_based_on_pattern
from .words import words, words_easy
from .models import Test, UsersScores, WordsSimMatrix
from .serializers import TestSerializer, UserScoresSerializer, WordsSimMatrixSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from auth_api.serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet
import pandas as pd

from pprint import pprint
# Create your views here.
from django.db.models import Q
class FetchWords(APIView):
    def get(self, request,mode,   length):
        print(length)
        words_to_display = words_easy if mode == "easy" else words
        word_list = pickRandValues(words_to_display, length)
        return Response({"words" : word_list}, status=status.HTTP_200_OK)


class TestView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    
class UserProfile(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    # permission_classes  = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # print(serializer.data)
        
        print(get_user_model().ROLES[serializer.data["role_id"]][1])
        return Response({
                    "error" : None,
                    "code" : 200,
                    "data" : {
                        **serializer.data,
                        "role_id" : get_user_model().ROLES[serializer.data["role_id"]][1]
                    },
                    "message" : "Success Fetching user profile"
                })

class TestResult(generics.CreateAPIView, generics.UpdateAPIView):
    # serializer_class = UsersScores
    # queryset = UsersScores.objects.all()

    def create(self, request, *args, **kwargs):
        # pprint(request.data["word_scored"])
        datas = request.data["word_scored"]
        # print(datas)
        serializer = UserScoresSerializer(data=datas, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(datas, status=status.HTTP_201_CREATED, headers=headers)
        # return Response(datas, status=status.HTTP_201_CREATED)




class GetRecommendation(generics.RetrieveAPIView):
    def retrieve(self, request, user_id, *args, **kwargs):
        if user_id == 0:
            word_list = pickRandValues(words, 90)
            return Response({"words" : word_list}, status=status.HTTP_200_OK) 
        
        usersscores = UsersScores.objects.all()
        score_serializer = UserScoresSerializer(usersscores, many=True)

        scores_df = pd.DataFrame(score_serializer.data)

        print(scores_df.head())
        # user_history = UsersScores.objects.all().filter(user_id=user_id)
        # history_serializer = UserScoresSerializer(user_history, many=True)

        print(user_id)
        all_user_data = scores_df.query(f"user_id == {user_id}")
        df= all_user_data.drop_duplicates(subset = ['user_id', 'item_id'], keep="last")
        highest_rating = df.sort_values(by='rating', ascending=False)
        print(highest_rating.head(20))
        if len(highest_rating) == 0:
            word_list = pickRandValues(words, 30)
            return Response({"words" : word_list}, status=status.HTTP_200_OK) 
        print(highest_rating.iloc[:10,3].tolist())


        matrix = WordsSimMatrix.objects.filter(word__in= highest_rating.iloc[:2,3].tolist())
        serializer = WordsSimMatrixSerializer(matrix, many=True)
        data = serializer.data

        words_list = recommend_words_based_on_pattern(data, 25)
        words_list2 = recommend_words_based_collaborative(scores_df, user_id, 40)
        words_all = [*words_list, *words_list2]
        return Response({
            "words": words_all,
            # "words" : pickRandValues(words_all, 90)
        }, status=status.HTTP_200_OK)