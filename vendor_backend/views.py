from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterUserForm, StationForm
import os
import numpy as np
import math
from collections import defaultdict

from django.db.models import Count
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
from .latlon import NYC_LOCATIONS


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
	return redirect('home')


def store_station(request):
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            selected_option = form.cleaned_data['stations']
            GotoLocationRequest.objects.create(user = request.user, region = selected_option)
            return redirect('/api/profit_ranking')
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
			return redirect('home')
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
        location_counts = GotoLocationRequest.objects.filter(timestamp__gte=one_hour_ago) \
                                             .values('region') \
                                             .annotate(count=Count('region')) \
                                             .order_by('region')


        region_to_food_vendors = defaultdict(int)
        for location in location_counts:
            print(f"Location: {location['region']}, Count: {location['count']}")
            region_to_food_vendors[location['region']] = location['count']
                
        region_total = defaultdict(int)
        for d in data:
            region = d['region']
            activity = d['total_activity']
            if region not in region_total:
                region_total[region] = 0
            region_total[region] += activity


        values = [(region_total[region] / (1+0.4*region_to_food_vendors[region] ** 1/3)) for region in region_total]
        mean = np.mean(values)
        sd = np.std(values)
        for region in region_total:
            region_total[region] /= (1 + region_to_food_vendors[region]**(1/3))
            region_total[region] -= mean
            region_total[region] /= sd
            region_total[region] *= 10
            region_total[region] += 100

        
        
        
        sorted_list = sorted(region_total.items(), key=lambda x: -x[1])

        regions = [(region, idx + 1, round(score, 2), ) for idx, (region, score) in enumerate(sorted_list)]


        map = folium.Map(location=[40.7128, -74.0060], zoom_start=12)
        heatmap_data = [(*NYC_LOCATIONS[region], score) for (region, score) in sorted_list]
        HeatMap(data=[(lat, lon, score) for lat, lon, score in heatmap_data]).add_to(map)

        map_html = map._repr_html_()
        print(map_html)
        
        return render(request, 'profit_view.html', {'regions': regions, 'map_html': map_html})





