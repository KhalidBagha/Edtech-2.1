from dataclasses import fields
from rest_framework import serializers
from .models import *

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model =Assignments
        fields = ['name','description']

    name=serializers.CharField(max_length=200)
    description=serializers.CharField(max_length=500)
    # date=serializers.DateTimeField(source='date_created')  #changing name as in model
    # xyz=serializers.SerializerMethodField(method_name='custom')  # our own field in serializer
  

    # def custom(self,assignment:Assignments):
    #     return 'ABC'

class StudentSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    username=serializers.CharField()
  
  
class SubmitAssignSerializer(serializers.ModelSerializer):  #using Model Serializer
    class Meta:
        model =SubmitAssignments
        fields =['student','assignment','description']
        
    student = serializers.HyperlinkedRelatedField(
         queryset = User.objects.all(),
         view_name='atd')



class MyAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignments
        fields = ['name','description','submission_counts']
    submission_counts = serializers.IntegerField()
        
          
    
# class SubmitAssignSerializer(serializers.Serializer):            ## USing Serializer
#     # student = serializers.StringRelatedField()  another way to related field
#     student = serializers.HyperlinkedRelatedField(
#         queryset = User.objects.all(),
#         view_name='studentsubmit')
#     assignment = serializers.StringRelatedField()
#     description=serializers.CharField(max_length=500)
#     date_created=serializers.DateTimeField()