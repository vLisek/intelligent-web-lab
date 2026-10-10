from flask import Flask, jsonify, request
import math

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "nazwa": "Klawiatura mechaniczna", "kategoria": "akcesoria", "cena": 349.99, "opis": "Przełączniki hot-swap, podświetlenie RGB"},
    {"id": 2, "nazwa": "Mysz bezprzewodowa", "kategoria": "akcesoria", "cena": 129.00, "opis": "Ciche przyciski, 4000 DPI"},
    {"id": 3, "nazwa": "Monitor 27 cali", "kategoria": "monitory", "cena": 1099.00, "opis": "Matryca IPS, 144 Hz"},
    {"id": 4, "nazwa": "Słuchawki nauszne", "kategoria": "audio", "cena": 449.00, "opis": "ANC, 40 h pracy na baterii"},
    {"id": 5, "nazwa": "Hub USB-C", "kategoria": "akcesoria", "cena": 199.00, "opis": "HDMI, 3x USB-A, czytnik SD"},
]

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/products")
def products():
    max_price = request.args.get("max_price")

    if max_price is None:
        return jsonify(PRODUCTS), 200

    try:
        max_price = float(max_price)
    except ValueError:
        return jsonify({"error": "Invalid max_price"}), 400

    if not math.isfinite(max_price) or max_price < 0:
        return jsonify({"error": "Invalid max_price"}), 400

    filtered_products = [
        product for product in PRODUCTS
        if product["cena"] <= max_price
    ]

    return jsonify(filtered_products), 200




@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = next(
        (p for p in PRODUCTS if p["id"] == product_id),
        None
    )

    if product is None:
        return jsonify({"error": "not found"}), 404

    return jsonify(product), 200


if __name__ == "__main__":
    app.run(debug=True)