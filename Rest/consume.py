from urllib import response
import requests


#Helps you to consume apis
response = requests.get('http://127.0.0.1:8000/drinks')
print(response.json())
