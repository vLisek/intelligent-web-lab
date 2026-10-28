from flask import Flask, jsonify, request

from recommender import matrix, recommend

app = Flask(__name__)


@app.route("/api/recommend")
def api_recommend():
    user = request.args.get("user", "").strip()
    if not user:
        return jsonify({"error": "podaj parametr ?user=..."}), 400

    k = request.args.get("k", type=int) if "k" in request.args else 3
    if k is None or not 1 <= k <= 11:
        return jsonify({"error": "k musi byc z zakresu 1-11"}), 400

    recs = recommend(user, k=k)
    if recs is None:
        return jsonify({
            "error": "nie znam takiego uzytkownika",
            "known_users": sorted(matrix.index.tolist()),
        }), 404

    return jsonify({"user": user, "k": k, "count": len(recs), "recommendations": recs})

@app.route("/api/users")
def api_users():
    users = sorted(matrix.index.tolist())
    return jsonify({"count": len(users), "users": users})


if __name__ == "__main__":
    app.run(debug=True)