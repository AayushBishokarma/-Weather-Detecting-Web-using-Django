from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
import json
import urllib.request
from datetime import datetime
x=datetime.now()
y=x.strftime('%d/%m/%Y') 


# Create your views here.
def index(request):
	if request.method=='POST':
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		password2 = request.POST['password2']

		if password == password2:
			if User.objects.filter(email=email).exists():
				messages.info(request,'Email Already Used :(')
				return redirect('index')
			elif User.objects.filter(username=username).exists():
				messages.info(request,'Username Already Exists :(  Try with another one.')
				return redirect('index')
			else:
				user = User.objects.create_user(username=username,email=email,password=password)
				user.save();
				return redirect('login')
		else:
			messages.info(request,'Password doesnot match :(')
			return redirect('index')
	else:
		return render(request,'index.html')


  
def login(request):
	
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username=username , password=password)

		if user is not None:
			auth.login(request, user)
			return redirect('weather')
		else:
			messages.info(request,'Invalid Credentials.Please try again :)')
			return redirect('login')

	else:
		return render(request,'login.html')

def log(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = auth.authenticate(username=username , password=password)

		if user is not None:
			auth.login(request, user)
			return redirect('weather')
		else:
			messages.info(request,'Invalid Credentials.Please try again :)')
			return redirect('log')

	else:
		return render(request,'log.html')





def weather(request):
    if request.method == 'POST':
        city = request.POST['city']
        res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=cb771e45ac79a4e8e2205c0ce66ff633').read()
        json_data = json.loads(res)
        data = {
            "country_code": str(json_data['sys']['country']),
            "coordinate": str(json_data['coord']['lon']) + ' to ' +
            str(json_data['coord']['lat']),
            "temp": str(int(json_data['main']['temp']) - 273) + chr(176) +'C' ,
            "pressure": str(json_data['main']['pressure']) + ' Pa',
            "humidity": str(json_data['main']['humidity']) + ' %',

        }


    else:
        city = ''
        data = {}
    return render(request, 'weather.html', {'city': city, 'data': data,'time':x})

