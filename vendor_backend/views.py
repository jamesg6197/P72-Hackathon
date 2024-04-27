from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login, logout
from .forms import SignUpForm, LoginForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta
from .models import ActivityHeatmapData

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
    
class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'vendor_backend/html_forms/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginView(generic.FormView):
    form_class = LoginForm
    success_url = reverse_lazy('home')
    template_name = 'vendor_backend/html_forms/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)
    

def logout_view(request):
    logout(request)
    return redirect('login')






