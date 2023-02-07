from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ClassListView, StudentListView, Home, ClassCreateView, StudentCreateView, ClassUpdate, ClassDelete, StudentDetails, StudentUpdate, StudentRemove, SubjectNew, SubjectUpdate, SubjectDelete, Results, ResultPdf, signup, Index, logout_view
from .forms import LoginForm
urlpatterns = [
    path('class_space', Home.as_view(), name='home'),
    path('', Index.as_view(), name='index'),
    path('class', ClassListView.as_view(), name='class'),
    path('student/<int:pk>', StudentListView.as_view(), name='student'),
    path('class/new', ClassCreateView.as_view(), name='newclass'),
    path('student/new/<int:pk>', StudentCreateView.as_view(), name='newstudent'),
    path('class/<int:pk>/edit', ClassUpdate.as_view(), name='editclass'),
    path('class/<int:pk>/delete', ClassDelete.as_view(), name='deleteclass' ),
    path('student/<int:pk>/details', StudentDetails.as_view(), name='studentdetails'),
    path('student/<int:pk>/update', StudentUpdate.as_view(), name='updatestudent'),
    path('student/<int:pk>/remove', StudentRemove.as_view(), name='removestudent'),
    path('subject/new/<int:pk>', SubjectNew.as_view(), name="subject"),
    path('subject/<int:pk>/update', SubjectUpdate.as_view(), name='subjectupdate'),
    path('subject/<int:pk>/delete', SubjectDelete.as_view(), name='deletesubject' ),
    path('results/<int:pk>/', Results.as_view(), name='results' ),
    path('result/<int:pk>/pdf', ResultPdf.as_view(), name='result_pdf' ),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    
]
