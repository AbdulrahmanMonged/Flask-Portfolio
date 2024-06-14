from config import app, api, email, URI
from flask import request
from flask_restful import Resource
import resend
import psycopg
import asyncio
import json
import datetime
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
@app.route("/")
def home():
    return "Hello World!"


async def get_from_db():
    async with await psycopg.AsyncConnection.connect(URI) as db:
        async with db.cursor() as cursor:
            await cursor.execute(
                    "SELECT * FROM OPERATIONS"
                )
            users = await cursor.fetchall()
            return [list(map(str, user)) for user in users]

class SendEmail(Resource):
    def post(self):
        try:
            data = request.get_json()
            params = {
                "from": "Your own Portfolio <onboarding@resend.dev>",
                "to": email,
                "subject": data["subject"]["value"],
                "html": "<p>Email: {0}</p><p>Subject: {2}</p><p>Message:</p><p style='white-space: pre-wrap;'>{1}</p>".format(
                    data["email"]["value"], data["message"]["value"], data["subject"]["value"]
                ),
            }
            resend.Emails.send(params)
            return "Sent Successfully!", 201
        except Exception as e:
            print(e)
            return "Error occured while validation Data", 400

class Database(Resource):
    def get(self):
        try:
            responses = asyncio.run(get_from_db())
            return responses, 200
        except Exception as e:
            print(e)
            
api.add_resource(SendEmail, "/email")
api.add_resource(Database, "/admin/db")
