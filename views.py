from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from .models import Contact,StudentCourse,Course

# Create your views here.
def scopehome(request):
    return render(request,'scopehome.html')

  
def scopeabout(request):
    return render(request,'scopeabout.html')

from django.core.mail import send_mail
from django.conf import settings
from .models import Contact

def scopecontact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        try:
            # ✅ Save to database
            Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            # ✅ Send email
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                ['info@scopeindia.org'],
            )

            # ✅ Show success ONLY when everything works
            return render(request, 'scopecontact.html', {'success': True})

        except:
            return render(request, 'scopecontact.html', {'error': True})

    return render(request, 'scopecontact.html')


import random
import string
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Student


def generate_temp_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))



from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .models import Student
from django.utils.crypto import get_random_string

temp_password = get_random_string(length=8)

def register(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        gender = request.POST.get('gender')
        dob_str = request.POST.get('dob')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')

        # ✅ FIX hobbies (multiple values)
        hobbies_list = request.POST.getlist('hobbies')
        hobbies = ','.join(hobbies_list)

        # ✅ FIX avatar (FILES not POST)
        avatar = request.FILES.get('avatar')

        # ✅ FIX date conversion
        try:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        except:
            messages.error(request, "Invalid date format. Use YYYY-MM-DD")
            return redirect('register')

        # Check duplicate email
        if Student.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        # Generate temporary password
        temp_password = get_random_string(8)

        # Save data
        student = Student.objects.create(
            firstname=firstname,
            lastname=lastname,
            gender=gender,
            dob=dob,
            email=email,
            password=temp_password,
            phonenumber=phonenumber,
            country=country,
            state=state,
            city=city,
            hobbies=hobbies,
            avatar=avatar
        )

        # Send email to company
        send_mail(
            subject="New Student Registration",
            message=f"""
New student registered:

Name: {firstname} {lastname}
Email: {email}
Phone: {phonenumber}

Temporary Password: {temp_password}
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        # Send email to user
        send_mail(
            subject="Your Account Created",
            message=f"""
Hello {firstname},

Your account has been created.

Temporary Password: {temp_password}

Please login and change your password.
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, "Registered successfully! Check your email.")
        return redirect('login')

    return render(request, 'registration.html')

# views.py
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Student

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Student.objects.get(email=email)

            # ✅ Only use user INSIDE try block
            if user.password == password:
                request.session['user_id'] = user.id
                return redirect('dashboard')
            else:
                messages.error(request, "Wrong password")

        except Student.DoesNotExist:
            messages.error(request, "User not found")

    return render(request, 'login.html')
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = Student.objects.get(email=email)

            temp_password = get_random_string(8)

            user.password = temp_password
            user.must_change_password = True  # 🔥 force reset
            user.save()

            send_mail(
                "Temporary Password",
                f"Your temporary password: {temp_password}",
                settings.EMAIL_HOST_USER,
                [email],
            )

            messages.success(request, "Temp password sent to email")

        except Student.DoesNotExist:
            messages.error(request, "Email not found")

    return render(request, 'forgot.html')

def change_password(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = Student.objects.get(id=user_id)

    if request.method == "POST":
        new_password = request.POST.get('password')

        if not new_password:
            messages.error(request, "Password cannot be empty")
            return redirect('change_password')

        # ✅ SAVE NEW PASSWORD
        user.password = new_password
        user.must_change_password = False
        user.save()   # 🔥 VERY IMPORTANT

        messages.success(request, "Password updated successfully!")
        return redirect('login')

    return render(request, 'change_password.html')
# views.py
from django.shortcuts import render, redirect
from .models import Course

from .models import Course, Student, StudentCourse

def dashboard(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    student = Student.objects.get(id=user_id)

    query = request.GET.get('search')

    if query:
        courses = Course.objects.filter(name__icontains=query)
    else:
        courses = Course.objects.all()

    if request.method == "POST":
        course_id = request.POST.get('course_id')
        course = Course.objects.get(id=course_id)

        if not StudentCourse.objects.filter(student=student, course=course).exists():
            StudentCourse.objects.create(student=student, course=course)

        messages.success(request, "Course signed up successfully!")
        return redirect('dashboard')

    picked = StudentCourse.objects.filter(student=student)

    return render(request, 'dashboard.html', {
    
        'courses': courses,
        'picked': picked,
        'user': student
    })
def logout_view(request):
    request.session.flush()
    response = redirect('login')
    response.delete_cookie('user_email')
    return response

def search_courses(request):
    query = request.GET.get('q')

    courses = Course.objects.filter(name__icontains=query)

    return render(request, 'dashboard.html', {'courses': courses})

def signup_course(request, course_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    student = Student.objects.get(id=user_id)
    course = Course.objects.get(id=course_id)

    # جلوگیری duplicate signup
    if not StudentCourse.objects.filter(student=student, course=course).exists():
        StudentCourse.objects.create(student=student, course=course)

    messages.success(request, "Course signed up successfully!")
    return redirect('dashboard')
def my_courses(request):
    user_id = request.session.get('user_id')
    student = Student.objects.get(id=user_id)

    courses = StudentCourse.objects.filter(student=student)

    return render(request, 'my_courses.html', {'courses': courses})
def profile(request):
    user_id = request.session.get('user_id')

    user = Student.objects.get(id=user_id)

    if request.method == "POST":
        user.firstname = request.POST.get('firstname')
        user.lastname = request.POST.get('lastname')
        user.phonenumber = request.POST.get('phonenumber')
        user.save()

        messages.success(request, "Profile updated!")
        return redirect('dashboard')

    return render(request, 'profile.html', {'user': user})

from django.shortcuts import render, redirect
from .models import Student

def change_password(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = Student.objects.get(id=user_id)

    if request.method == "POST":
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        # Check existing password
        if user.password == old_password:
            user.password = new_password
            user.save()

            # Logout after password change
            request.session.flush()

            return redirect('login')  # redirect to login page

        else:
            return render(request, 'change_password.html', {
                'error': 'Incorrect existing password'
            })

    return render(request, 'change_password.html')

    
def logout_view(request):
    request.session.flush()
    response = redirect('login')
    response.delete_cookie('user_email')
    return response