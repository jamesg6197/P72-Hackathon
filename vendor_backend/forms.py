from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterUserForm(UserCreationForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(RegisterUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'
		
class StationForm(forms.Form):
    STATION_CHOICES = [
        ('Times Square', 'Times Square'),
        ('Central Park', 'Central Park'),
        ('Statue of Liberty', 'Statue of Liberty'),
        ('Empire State Building', 'Empire State Building'),
        ('Brooklyn Bridge', 'Brooklyn Bridge'),
        ('Metropolitan Museum of Art', 'Metropolitan Museum of Art'),
        ('One World Trade Center', 'One World Trade Center'),
        ('Yankee Stadium', 'Yankee Stadium'),
        ('Coney Island', 'Coney Island'),
        ('Prospect Park', 'Prospect Park'),
        ('Flushing Meadows Corona Park', 'Flushing Meadows Corona Park'),
        ('JFK Airport', 'JFK Airport'),
        ('LaGuardia Airport', 'LaGuardia Airport'),
        ('Bronx Zoo', 'Bronx Zoo'),
        ('New York Botanical Garden', 'New York Botanical Garden'),
        ('Museum of Modern Art', 'Museum of Modern Art'),
        ('Rockefeller Center', 'Rockefeller Center'),
        ('Wall Street', 'Wall Street'),
        ('The High Line', 'The High Line'),
        ('Carnegie Hall', 'Carnegie Hall'),
        ('Madison Square Garden', 'Madison Square Garden'),
        ('Battery Park', 'Battery Park'),
        ('Greenwich Village', 'Greenwich Village'),
        ('Ellis Island', 'Ellis Island'),
        ('Staten Island Ferry', 'Staten Island Ferry'),
        ('Apollo Theater', 'Apollo Theater'),
        ('Harlem', 'Harlem'),
        ('Queens Museum', 'Queens Museum'),
        ('Museum of the Moving Image', 'Museum of the Moving Image'),
        ('Fordham University', 'Fordham University'),
        ('Columbia University', 'Columbia University'),
        ('New York University', 'New York University'),
        ('Brooklyn Botanic Garden', 'Brooklyn Botanic Garden'),
        ('Prospect Park Zoo', 'Prospect Park Zoo'),
        ('Williamsburg, Brooklyn', 'Williamsburg, Brooklyn'),
        ('Bushwick, Brooklyn', 'Bushwick, Brooklyn'),
        ('Astoria, Queens', 'Astoria, Queens'),
        ('Long Island City, Queens', 'Long Island City, Queens'),
        ('Forest Hills, Queens', 'Forest Hills, Queens'),
        ('Flatbush, Brooklyn', 'Flatbush, Brooklyn'),
        ('Park Slope, Brooklyn', 'Park Slope, Brooklyn'),
        ('Red Hook, Brooklyn', 'Red Hook, Brooklyn'),
        ('Dumbo, Brooklyn', 'Dumbo, Brooklyn'),
        ('Chelsea, Manhattan', 'Chelsea, Manhattan'),
        ('SoHo, Manhattan', 'SoHo, Manhattan'),
        ('Tribeca, Manhattan', 'Tribeca, Manhattan'),
        ('Upper East Side, Manhattan', 'Upper East Side, Manhattan'),
        ('Upper West Side, Manhattan', 'Upper West Side, Manhattan'),
        ('Lower East Side, Manhattan', 'Lower East Side, Manhattan'),
        ('Chinatown, Manhattan', 'Chinatown, Manhattan'),
        ('Harlem, Manhattan', 'Harlem, Manhattan'),
        ('Financial District, Manhattan', 'Financial District, Manhattan'),
        ('Midtown Manhattan', 'Midtown Manhattan')        
    ]
    stations = forms.ChoiceField(choices=STATION_CHOICES)
