from config import app, api, email
from flask import request
from flask_restful import Resource
import resend


@app.route("/")
def home():
    return "Hello World!"


class SendEmail(Resource):
    def post(self):
        try:
            data = request.get_json()
            params = {
                "from": "Your own Portfolio <onboarding@resend.dev>",
                "to": email,
                "subject": data["subject"],
                "html": """<!DOCTYPE html>
                <html>
                <head>
                <style>
    body {
      font-family: Arial, sans-serif;
    }
    .container {
      width: 80%;
      margin: auto;
      padding: 20px;
      border: 1px solid #ddd;
      border-radius: 5px;
      background-color: #f9f9f9;
    }
    .header {
      text-align: center;
      margin-bottom: 20px;
    }
    .content {
      margin-bottom: 20px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Hello there!</h1>
    </div>
    <div class="content">
      <p>Email: {0}</p>
      <p>Subject: {2}</p>
      <p>Message:</p>
      <p style="white-space: pre-wrap;">{1}</p>
    </div>
  </div>
</body>
</html>""".format(
                    data["email"]["value"],
                    data["message"]["value"],
                    data["subject"]["value"],
                ),
            }
            resend.Emails.send(params)
            return "Sent Successfully!", 201
        except Exception as e:
            return "Error occured while validation Data", 400


api.add_resource(SendEmail, "/email")
