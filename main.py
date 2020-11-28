from flask import Flask, render_template, request
import config
import sendgrid
from twython import Twython, TwythonError
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

            SENDGRID_API_KEY = Twython.(config.api_key)
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