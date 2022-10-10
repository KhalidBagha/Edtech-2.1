from itertools import product
from django.shortcuts import render,redirect,get_object_or_404
from django.http import request
from django.contrib.auth.models import User,Group
from .models import *
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .forms import *
from .decorators import * 








##########

##########
    #API
##########

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
@api_view()
def assign_list(request):
    query = Assignments.objects.all()
    se = AssignmentSerializer(query,many=True)
    return Response(se.data)

@api_view()
def assign_listbyid(request,pk):
    ass = get_object_or_404(Assignments,id= pk)
    s = AssignmentSerializer(ass)
    return Response(s.data)

@api_view(['GET','POST'])
def submit_assignlist(request):
    if request.method == 'GET':
        query = SubmitAssignments.objects.all()
        se = SubmitAssignSerializer(query,many=True,context = {'request':request})
        return Response(se.data)
    elif request.method == 'POST':
        serializer = SubmitAssignSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer._validated_data)
        return Response("OKAY")
        
    


@api_view(['GET','PUT','DELETE'])
def student_detail_apiView(request,pk):
    subass = get_object_or_404(SubmitAssignments,id=pk)
    if request.method == "GET":
        ser = SubmitAssignSerializer(subass,context={'request': request})
        return Response(ser.data)
    elif request.method == 'PUT':
        ser = SubmitAssignSerializer(subass,data = request.data,context={'request': request})
        ser.is_valid()
        ser.save()
        return Response(ser.data)
    elif request.method == 'DELETE':
        subass.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
        
class SAVEASSIGN(ListCreateAPIView):
    queryset = Assignments.objects.all()
    serializer_class = AssignmentSerializer
    def get_serializer_context(self):
        return {'request': request}
    
############## Converting student_detail_apiView to class based view


# class StudentDetailApiView(APIView):
    # def get(self,request,pk):
    #     subass = get_object_or_404(User,id=pk)
    #     ser = StudentSerializer(subass,context={'request': request})
    #     return Response(ser.data)
    
    # def put(self,request,pk):
    #     subass = get_object_or_404(User,id=pk)
    #     ser = StudentSerializer(subass,data = request.data,context={'request': request})
    #     print(ser)
    #     ser.is_valid()
    #     ser.save()
    #     return Response(ser.data)
    
    # def delete(self,request,pk):
    #     subass = get_object_or_404(User,id=pk)
    #     subass.delete()
    #     return Response(status = status.HTTP_204_NO_CONTENT)
 
 
 
############# Generic views

class StudentDetailApiView(ListCreateAPIView):
    queryset =  Assignments.objects.all()
    serializer_class = AssignmentSerializer
    def get_serializer_context(self):
        return {'request':self.request}


# @api_view(['GET','POST'])
# def assignmentList(request):
#     query = Assignments.objects.annotate(submission_counts = count('SubmitAssignments')).all()
    
 
 
 
class AssignmentViewSets(ModelViewSet):
    queryset =  Assignments.objects.all()
    serializer_class = AssignmentSerializer
    
    def get_serializer_context(self):
        return {'request':self.request}

 
 
 
##########
 


##########
##########




# Create your views here.
@unauthenticated_user
def signupuser(request):
    
    form = CreateUserForm()
    context = {'form':form}
    if request.method =='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            group = Group.objects.get(name="student")
            user.groups.add(group)
            
            return redirect("login")
        else:
            print(form.errors)
    return render(request,'signup.html',context)


    # if request.method == 'POST':
    #     try:
    #         u_name= request.POST.get('username')
    #         u_email= request.POST.get('email')
    #         u_pass1= request.POST.get('password')
    #         u_pass2= request.POST.get('c_password')
            
    #         if u_pass1 == u_pass2:
    #             user = User.objects.create(username = u_name,email = u_email,password =u_pass1 )
    #             group = Group.objects.get(name="student")
    #             user.groups.add(group)
    #             print(u_name,u_email,u_pass1,u_pass2,group)
    #             return redirect('login')
            
    #     except:
    #         print("SignUp Failed")
            
    # return render(request,'signup.html')

@unauthenticated_user
def Login(request):
    if request.method == 'POST':
        try:
            u_name= request.POST.get('username')
            u_pass1= request.POST.get('password')
            user= authenticate(request,username=u_name,password=u_pass1)
            print(user,u_name,u_pass1)
            if user is not None:
                login(request,user)
                return redirect('dash')
            else:
                return render(request,'login.html')

        except:
            print("Login Failed")
            
    return render(request,'login.html')

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('login')    


@login_required(login_url='login')
@admin_only

def adminDashboard(request):
    assignment  = Assignments.objects.all()
    students  = User.objects.filter(groups__name= "student").count()
    print(students)


    from datetime import datetime, timedelta

    today = datetime.now()
    six_days_ago_date = (today - timedelta(days=6)).date()
    print(six_days_ago_date)

    totalsubmissions  = SubmitAssignments.objects.all().count()
    admins  = User.objects.filter(groups__name= "admin").count()
    context = {'assignments':assignment,'students':students,'totalsubmissions':totalsubmissions,'admins':admins}



    return render(request,'abc.html',context)

@login_required(login_url='login')
def studentpanel(request):
    assignment  = Assignments.objects.all()
    assignment2  = SubmitAssignments.objects.filter(student = request.user.id)

    print([x.id for x in assignment2])

  
    context = {'assignments':assignment,'assignmentss':assignment2}
    return render(request,'studentpanel.html',context)

@login_required(login_url='login')

def exercises(request,pk):
    assignment = Assignments.objects.get(id=pk)
    context = {'assignments':assignment}
    if request.method == "POST":
        inp = request.POST.get('u_input')
        user = User.objects.get(id= request.user.id )
        saving = SubmitAssignments.objects.create(student = user, assignment = assignment,description = inp)
        if saving :
             return redirect('studentpanel')
            
        print(request.user.id,inp,pk)
    return render(request,'exercise.html',context)


@login_required(login_url='login')
@admin_only

def create_assignments(request):
    if request.method == "POST":
        ass_name= request.POST.get('assignment_name')
        ass_desc= request.POST.get('assignment_description')
        p = Assignments.objects.create(name=ass_name,description=ass_desc)
        return redirect('dash')
    # order = Order.objects.get(id = pk)
    
    # form = OrderForm(instance=order)

    # context = {'form':form}
    
    return render(request,'create_assignment.html')
