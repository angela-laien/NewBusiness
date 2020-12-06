from flask import Flask, render_template, request
import sendgrid
import os
from sendgrid.helpers.mail import Email
from sendgrid.helpers.mail import Content
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
@app.route("/index.html", methods=['POST', 'GET'])

def index():
    if request.method == 'POST':
        email_address = request.form['email']
        full_name = request.form['name']
        message = request.form['message']

        if email_address != '':
            full_name = full_name.encode('ascii', errors="ignore").decode()

            SENDGRID_API_KEY = os.getenv('API_KEY')
            print(SENDGRID_API_KEY)
            sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

            message = Mail(
                from_email='laienxie@gmail.com',
                to_emails='laienxie@gmail.com',
                subject='New SFPreloved.com Message',
                html_content='Email: ' + email_address + ' Name: ' + full_name + ' ' + message
            )

            try:
                sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
                response = sg.send(message)
            except Exception as e:
                print(str(e))

    return render_template("index.html")

import pygeoip, time
from datetime import datetime
import base64

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
geo = pygeoip.GeoIP(os.path.join(BASE_DIR, 'GeoLiteCity.dat'))

def pixel_tracker():
    # <img src="https//sfpreloved.herokuapp.com/pixel.gif?page=index.html" style="width: 1px; height: 1px" />
    origin_page = 'nowhere'
    geo_data = 'nowhere'
    client_ip = ''
    if 'page' in request.args:
        origin_page = request.args.get('page')

        # visitor IP
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

        # visitor referrer
        referrer = request.headers.get("Referer")

        # location of visitor - wont' work on free PythonAnywhere accounts
        # url = 'https://freegeoip.app/json/{}'.format(client_ip)
        # r = requests.get(url)
        # j = json.loads(r.text)

        # https://pygeoip.readthedocs.io/en/v0.3.2/index.html
        # https://github.com/walchko/Python/blob/master/network_python/geolocate/GeoLiteCity.dat
        geo_data = geo.country_name_by_addr(client_ip)

    # encoded pixel image https://github.com/sethblack/python-flask-pixel-tracking/blob/master/pfpt/main.py
    pixel_data = base64.b64decode("R0lGODlhAQABAIAAAP8AAP8AACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==")

    # log traffic to file
    st = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    # save to file and send thank you note
    with open("pixel-tracker.csv","a") as myfile:
        myfile.write('Timestamp: ' + st + ' origin_page:' + origin_page +
            ' client_ip: ' + client_ip + ' referrer:' + referrer + ' geo:' + str(geo_data) + '\n')

    return Response(pixel_data, mimetype="image/gif")