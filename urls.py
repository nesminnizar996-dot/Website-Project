from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns=[
    path('home/',views.scopehome,name='home'),
    path('about',views.scopeabout,name='about'),
    path('contact',views.scopecontact,name='contact'),
    path('registration',views.register,name='register'),
    path('login/', views.login_view, name='login'),
    path('forgot/', views.forgot_password, name='forgot_password'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search/', views.search_courses, name='search'),
    path('signup-course/<int:course_id>/', views.signup_course, name='signup_course'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('logout/', views.logout_view, name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    
    
