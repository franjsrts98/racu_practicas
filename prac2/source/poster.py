import requests
import json
import sys
from collections import OrderedDict

# CLIENTE HTTP
# Uso: poster.py <archivo.json>

# DIRECCION URL DEL SERVIDOR
url = 'http://212.128.44.107:8000'
print('Target URL: '+url)

def test_connection():
	print("Testing connection...")

	try:
		r = requests.get(url,timeout=5)
	except requests.exceptions.ConnectTimeout:
		print("(!) Connection timed out")
		return

	if (r.status_code == 200):
		print("Connection OK - Sending payload...")
		post_data()
	else:
		print("(!) Connection failed - Status code: "+r.status_code)

def post_data():
	try:
		r = requests.post(url,data=payload,timeout=5)
	except requests.exceptions.ConnectTimeout:
		print("(!) Connection timed out")
		return

	if (r.status_code == 200):
		print("Payload sent successfully! \n")
		print(r.text)
	else:
		print("(!) Payload not sent - Status code: "+r.status_code)

valid_payload = False
actual_payload = None

if len(sys.argv) == 2:
	try:
		with open(str(sys.argv[1])) as file:
			data = json.load(file,object_pairs_hook=OrderedDict)
			actual_payload = data
			valid_payload = True
	except ValueError as ve:
		print("(!) Invalid data (ValueError)")
	except TypeError as te:
		print("(!) Invalid data (TypeError)")

if valid_payload is False:
	print("Generating default payload...")
	payload = json.dumps({"temp":"-273.15","hum":"0","press":"0","location":"outer_space"})
else:
	payload = json.dumps(actual_payload)

test_connection()
