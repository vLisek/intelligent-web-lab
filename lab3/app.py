from flask import Flask, jsonify, request

from recommender import matrix, recommend, similar_users

app = Flask(__name__)


def unknown_user():
    return jsonify({
        "error": "nie znam takiego uzytkownika",
        "known_users": sorted(matrix.index.tolist()),
    }), 404


@app.route("/api/recommend")
def api_recommend():
    user = request.args.get("user", "").strip()
    if not user:
        return jsonify({"error": "podaj parametr ?user=..."}), 400

    k = request.args.get("k", type=int) if "k" in request.args else 3
    if k is None or not 1 <= k <= 11:
        return jsonify({"error": "k musi byc z zakresu 1-11"}), 400

    top_n = request.args.get("top_n", type=int) if "top_n" in request.args else 5
    if top_n is None or not 1 <= top_n <= 10:
        return jsonify({"error": "top_n musi byc z zakresu 1-10"}), 400

    recs = recommend(user, top_n=top_n, k=k)
    if recs is None:
        return unknown_user()

    return jsonify({"user": user, "k": k, "count": len(recs), "recommendations": recs})


@app.route("/api/similar")
def api_similar():
    user = request.args.get("user", "").strip()
    if not user:
        return jsonify({"error": "podaj parametr ?user=..."}), 400

    similar = similar_users(user)
    if similar is None:
        return unknown_user()

    return jsonify({"user": user, "similar": similar})


@app.route("/api/users")
def api_users():
    users = sorted(matrix.index.tolist())
    return jsonify({"count": len(users), "users": users})


if __name__ == "__main__":
    app.run(debug=True)