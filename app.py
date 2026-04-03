from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from config import MONGO_URI
from datetime import datetime

app = Flask(__name__)
CORS(app)

client = MongoClient(MONGO_URI)
db = client.money_manager
collection = db.transactions
users_collection = db.users

# GET all transactions
@app.route('/transactions', methods=['GET'])
def get_transactions():
    data = []
    for t in collection.find():
        data.append({
            "id": str(t["_id"]),
            "type": t["type"],
            "amount": t["amount"],
            "category": t["category"]
        })
    return jsonify(data)

# Auth endpoints
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400
        
    if users_collection.find_one({"username": username}):
        return jsonify({"message": "User already exists"}), 400
        
    users_collection.insert_one({"username": username, "password": password})
    return jsonify({"message": "Registered successfully"}), 201

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = users_collection.find_one({"username": username, "password": password})
    if user:
        return jsonify({"message": "Login successful", "username": username}), 200
    return jsonify({"message": "Invalid username or password"}), 401

# ADD transaction
@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.json
    result = collection.insert_one({
        "type": data["type"],
        "amount": data["amount"],
        "category": data["category"]
    })
    return jsonify({"id": str(result.inserted_id)})

# DELETE transaction
@app.route('/transactions/<id>', methods=['DELETE'])
def delete_transaction(id):
    collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Deleted"})


# Analytics: receive events
@app.route('/analytics', methods=['POST'])
def track_event():
    data = request.json or {}
    event = {
        "type": data.get("type"),
        "payload": data.get("payload", {}),
        "timestamp": datetime.utcnow()
    }
    db.analytics.insert_one(event)
    return jsonify({"ok": True}), 201


# Analytics summary
@app.route('/analytics/summary', methods=['GET'])
def analytics_summary():
    page_views = db.analytics.count_documents({"type": "page_view"})
    adds = db.analytics.count_documents({"type": "add_transaction"})
    deletes = db.analytics.count_documents({"type": "delete_transaction"})
    total = db.analytics.count_documents({})
    return jsonify({
        "page_views": page_views,
        "adds": adds,
        "deletes": deletes,
        "total_events": total
    })

if __name__ == "__main__":
    app.run(debug=True)