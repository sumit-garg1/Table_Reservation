#This is the part of frontend developnment part

from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib import messages


#This is the api part for create,delete,update
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Table, Reservation
from .serializers import TableSerializer,ReservationSerializer

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirmpass = request.POST.get('confirm-password')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already taken"})

        # Check if passwords match
        if password != confirmpass:
            return render(request, "signup.html", {"error": "Password and Confirm Password do not match"})

        # Create user
        User.objects.create_user(username=username, password=password)
        return redirect("login_view")  # Redirect to login after successful signup

    return render(request, "signup.html")


# --------------------------
# Login View (HTML)
# --------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})

    return render(request, "login.html")


@login_required
def home(request):
    if request.method == "POST":
        date = request.POST.get("date")
        time = request.POST.get("time")
        table_id = request.POST.get("table")

        table = Table.objects.get(id=table_id)

        # Check double booking
        if Reservation.objects.filter(table=table, date=date, time=time).exists():
            return render(request, "home.html", {"tables": Table.objects.all(), "error": "This table is already booked!"})

        Reservation.objects.create(table=table, user=request.user, date=date, time=time)
        return render(request, "home.html", {"tables": Table.objects.all(), "success": "Reservation successful!"})

    return render(request, "home.html", {"tables": Table.objects.all()})

# Create your views here.
class TableViewSet(viewsets.ModelViewSet):
    queryset=Table.objects.all()
    serializer_class=TableSerializer
    permission_classes=[IsAuthenticated]

    @action(detail=False,methods=['get'])
    def available(self,request):
        date = request.query_params.get('date')
        time = request.query_params.get('time')
        if not date or not time:
            return Response({"error": "date and time are required"}, status=400)
        
        booked_tables = Reservation.objects.filter(date=date, time=time).values_list('table_id', flat=True)
        available_tables = Table.objects.exclude(id__in=booked_tables)
        serializer = TableSerializer(available_tables, many=True)
        return Response(serializer.data)
class ReservationViewSet(viewsets.ModelViewSet):
    queryset=Reservation.objects.all()
    serializer_class=ReservationSerializer
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        table = serializer.validated_data['table']
        date = serializer.validated_data['date']
        time = serializer.validated_data['time']

        if Reservation.objects.filter(table=table,date=date,time=time).exists():
            raise serializers.ValidationError("This table is already booked for the selected date/time.")

        serializer.save(user=self.request.user)
@login_required
def cancel_reservation(request, pk):
    try:
        reservation = Reservation.objects.get(id=pk, user=request.user)
        reservation.delete()
    except Reservation.DoesNotExist:
        pass
    return redirect('reservation')

@login_required
def update_reservation(request, pk):
    reservation = Reservation.objects.get(id=pk, user=request.user)
    if request.method == "POST":
        reservation.date = request.POST.get("date")
        reservation.time = request.POST.get("time")
        reservation.table_id = request.POST.get("table")
        reservation.save()
        return redirect('reservation')

    return render(request, "update.html", {
        "reservation": reservation,
        "tables": Table.objects.all()
    })

@login_required
def reservation(request):
    reservations = Reservation.objects.filter(user=request.user)  # sirf current user ke reservations
    return render(request, "reservation.html", {"reservations": reservations})