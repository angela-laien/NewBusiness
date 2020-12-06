import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(os.getenv('API_KEY'))
from_email = Email("laienxie@gmail.com")
subject = "Hello World from the SendGrid Python Library!"
to_email = To("laienxie@gmail.com")
content = Content("text/plain", "Hello, Email!")
mail = Mail(from_email, to_email, subject, content)
response = sg.send(mail)
print(response.status_code)
print(response.body)
print(response.headers)