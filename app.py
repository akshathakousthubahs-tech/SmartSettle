from flask import Flask, request, jsonify, send_file
import pandas as pd
import json
from scheduler import schedule_transactions

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["file"]

    df = pd.read_csv(file)

    transactions = df.to_dict("records")

    assignments, cost = schedule_transactions(transactions)

    result = {
        "assignments": assignments,
        "total_cost": cost
    }

    with open("submission.json","w") as f:
        json.dump(result,f,indent=2)

    return jsonify(result)


@app.route("/download")
def download():

    return send_file("submission.json",as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)