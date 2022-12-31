from django.urls import path
from .views import ClassListView, StudentListView, Home, ClassCreateView, StudentCreateView, ClassUpdate, ClassDelete, StudentDetails, StudentUpdate, StudentRemove, SubjectNew, SubjectUpdate

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('class', ClassListView.as_view(), name='class'),
    path('student/<int:pk>', StudentListView.as_view(), name='student'),
    path('class/new', ClassCreateView.as_view(), name='newclass'),
    path('student/new', StudentCreateView.as_view(), name='newstudent'),
    path('class/<int:pk>/edit', ClassUpdate.as_view(), name='editclass'),
    path('class/<int:pk>/delete', ClassDelete.as_view(), name='deleteclass' ),
    path('student/<int:pk>/details', StudentDetails.as_view(), name='studentdetails'),
    path('student/<int:pk>/update', StudentUpdate.as_view(), name='updatestudent'),
    path('student/<int:pk>/remove', StudentRemove.as_view(), name='removestudent'),
    path('subject/new', SubjectNew.as_view(), name="subject"),
    path('subject/<int:pk>/update', SubjectUpdate.as_view(), name='subjectupdate')
    # path to delete student
    

]
