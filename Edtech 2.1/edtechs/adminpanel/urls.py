import abc
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register('myassignments',AssignmentViewSets)
print(router.urls)

urlpatterns = [
    # path('',include(router.urls)),
    path('',adminDashboard,name="dash"),
    path('createAssignment/', create_assignments,name = "createAssignment"),
    path('signup/', signupuser,name = "signup"),
    path('login/', Login,name = "login"),
    path('studentdashboard/',studentpanel,name = "studentpanel"),
    path('exercises/<str:pk>',exercises,name = "exercises"),
    path('logout/', logoutPage,name="logout"),
    # path('assignlist/', assign_list,name="api"),
    # path('abc/', submit_assignlist,name="apis"),
    # path('assignlistbyid/<int:pk>/', assign_listbyid,name="apibyid"),
    # # path('students/<int:pk>/', student_detail_apiView,name="studentsubmit"),
    # path('studentssss/', StudentDetailApiView.as_view(),name="atd"),
    # path('myassignmentsave/', SAVEASSIGN.as_view(),name="myassignmentsave")

]

