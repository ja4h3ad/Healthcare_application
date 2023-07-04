from flask import Flask, request
import os
import vonage
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
client = vonage.Client(
    key=os.getenv('VONAGE_API_KEY'),
    secret=os.getenv('VONAGE_API_SECRET')
)

insight_number = os.getenv('INSIGHT_NUMBER')
callback_url = os.getenv('INSIGHT_NUMBER_CALLBACK_WEBHOOK')


#Start the trigger
insight_trigger_json = client.number_insight.get_async_advanced_number_insight(
    number=insight_number,
    callback=os.getenv('INSIGHT_NUMBER_CALLBACK_WEBHOOK'),
    features={'cnam': {}}
)

# You can also pass in JSON
insight_trigger_json = client.number_insight.get_async_advanced_number_insight({
    "number": insight_number,
    "callback": os.getenv('INSIGHT_NUMBER_CALLBACK_WEBHOOK'),
    "features": {
        "cnam": {}
    }
})

# Get the response from api - the data will be available on callback webhook
pprint(insight_trigger_json)

@app.route("/webhooks/insight", methods=['GET', 'POST'])
def callback():
    data = request.get_json()
    pprint(data)
    return "Query Successful"

if __name__ == '__main__':
    app.run(debug=True, port = 3000)