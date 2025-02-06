from flask import Flask, jsonify, render_template
import requests
import gtfs_realtime_pb2

app = Flask(__name__, static_folder='static')

API_URL = "https://api.data.gov.my/gtfs-realtime/vehicle-position/ktmb"

@app.route('/')
def home():
    return render_template('index.html')  # Flask will look in the 'templates' folder by default

@app.route('/trains', methods=['GET'])
def get_trains():
    try:
        response = requests.get(API_URL)
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch data"}), 500
        
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)

        trains = []
        for entity in feed.entity:
            if entity.vehicle:
            if entity.vehicle:
                train_info = {
                    "id": entity.vehicle.vehicle.id,
                    "latitude": entity.vehicle.position.latitude,
                    "longitude": entity.vehicle.position.longitude
                }
                trains.append(train_info)

        return jsonify({"trains": trains})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
