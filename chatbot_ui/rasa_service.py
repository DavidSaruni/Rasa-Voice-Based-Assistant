import requests

async def rasa_response(message):
    # Send the user's message to the Rasa server and get the bot's response
    _url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {
        "sender": "test_user",
        "message": message
    }

    response = requests.post(_url, json=payload)
    bot_response = response.json()

    return {"message": bot_response}