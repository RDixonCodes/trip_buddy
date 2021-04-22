from django.shortcuts import render, redirect
from buddy_app.models import*
from django.contrib import messages
import bcrypt

def index(request):

    return render(request, 'welcome.html')

def create_user(request):
    if request.method == "POST":
        
        errors = User.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect('/')

        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_pw
        )
        request.session['logged_user'] = new_user.id

        return redirect('/user/hello')
    return redirect("/")
    # localhost:8000/dashboard

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email = request.POST['email'])

        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                request.session['logged_user'] = log_user.id
                return redirect('/user/hello')
        messages.error(request, "Email or password are incorrect.")
            
    return redirect("/")

def dashboard(request):
    
    context = {
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'all_trips': Trip.objects.all().order_by('-created_at')
        }
        
    return render(request, 'hello.html', context)

def create_trip(request):
    if request.method == 'POST':
        errors = Trip.objects.basic_validator(request.POST)
        
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/user/trip')
                
    else:
        user = User.objects.get(id=request.session['logged_user'])
        new_trip = Trip.objects.create(
            destination = request.POST['destination'],
            start_date = request.POST['start_date'],
            end_date = request.POST['end_date'],
            plan = request.POST['plan'],
            user_trip = user
                )
    return redirect(f'/user/hello')

def trip(request):
    context = {
        'logged_user' : User.objects.get(id=request.session['logged_user']),
        'all_trips': Trip.objects.all()
    }

    return render(request, 'create_trip.html', context)

def edit_trip(request, trip_id):
    
    trip = Trip.objects.get(id=trip_id)
    context = {
        'logged_user' : User.objects.get(id=request.session['logged_user']),
        'trip': trip
        
        
    }
    
    return render(request, 'edit_trip.html', context)

def updated_trip(request, trip_id):
    if request.method == 'POST':
        errors = Trip.objects.basic_validator(request.POST)
        
    if len(errors) > 0:
        
        for key, value in errors.items():
            messages.error(request, value)
        
        return redirect(f'/trip/{trip_id}/edit')
    else:
        update_trip = Trip.objects.get(id=trip_id)
        update_trip.destination = request.POST['destination']
        update_trip.start_date = request.POST['start_date']
        update_trip.end_date = request.POST['end_date']
        update_trip.plan = request.POST['plan']
        update_trip.save()
        messages.success(request, "Trip successfully updated")

        
    return redirect(f'/user/hello')

def view_trip(request, trip_id):
    context = {
        'logged_user' : User.objects.get(id=request.session['logged_user']),
        'trip' : Trip.objects.get(id=trip_id),

    }
    return render(request, 'view_trip.html', context)

def delete_trip(request, trip_id):
    if 'logged_user' not in request.session:
        messages.error(reques, "Please register or log in first")
    trip = Trip.objects.get(id=trip_id)
    trip.delete()
    return redirect(f'/user/hello')

def logout(request):
    request.session.flush()
    return redirect('/')



# Create your views here.
