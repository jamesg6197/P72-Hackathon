from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterUserForm, StationForm
import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from .models import ActivityHeatmapData, RegionalDataHeatmap, GotoLocationRequest
from django.contrib import messages

from django.views import View
from django.http import HttpResponse

from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta


import folium
from folium.plugins import HeatMap

class HeatmapAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        # Fetch the most recent date of entry
        latest_date = ActivityHeatmapData.objects.latest('timestamp').timestamp
        now = timezone.now()

    # Calculate the time two minutes ago
        two_minutes_ago = now - timedelta(minutes=2)
        count = ActivityHeatmapData.objects.count()
        print(f"Number of HeatmapData objects: {count}")
        # Fetch all entries from the most recent date
        data = ActivityHeatmapData.objects.filter(timestamp__gte=two_minutes_ago).values('latitude', 'longitude', 'intensity')
        print(f"Number of HeatmapData data objects: {data.count()}")

        # Create map centered around the average location
        if data:
            map_center = [sum(d['latitude'] for d in data) / len(data), 
                          sum(d['longitude'] for d in data) / len(data)]
            map = folium.Map(location=map_center, zoom_start=12)
            heat_data = [(d['latitude'], d['longitude'], d['intensity']) for d in data]
            HeatMap(heat_data).add_to(map)
        else:
            map = folium.Map(location=[0, 0], zoom_start=2)  # Default location if no data

        # Generate map HTML
        map_html = map._repr_html_()

        return HttpResponse(map_html, content_type='text/html')

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.success(request, ("There Was An Error Logging In, Try Again..."))	
			return redirect('login')	


	else:
		return render(request, 'login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, ("You Were Logged Out!"))
	return redirect('')


def store_station(request):
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            selected_option = form.cleaned_data['stations']
            GotoLocationRequest.objects.create(region = selected_option)
            return HttpResponse('Success!')
    else:
        form = StationForm()
    return render(request, 'gotorequest.html', {'form': form})

def register_user(request):
	if request.method == "POST":
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Registration Successful!"))
			return redirect('')
	else:
		form = RegisterUserForm()

	return render(request, f'signup.html', {
		'form':form,
		})

def home(request):
    # Add any context data you need to pass to the template here
    context = {}
    return render(request, 'home.html', context)
class ProfitView(View):
    def get(self, request):
        now = timezone.now()
        one_hour_ago = now - timedelta(minutes=60)
        data = RegionalDataHeatmap.objects.filter(timestamp__gte=one_hour_ago).values('region', 'total_activity')
        
        region_total = {}
        for d in data:
            region = d['region']
            activity = d['total_activity']
            if region not in region_total:
                region_total[region] = 0
            region_total[region] += activity
        
        sorted_list = sorted(region_total.items(), key=lambda x: -x[1])
        regions = [(region, idx + 1) for idx, (region, _) in enumerate(sorted_list)]
        
        return render(request, 'profit_view.html', {'regions': regions})





