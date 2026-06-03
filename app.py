from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello_world_api():
    return jsonify({
        "status": "success",
        "message": "Hello from Flask"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)