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

# --- ZADANIE A: Filtr ceny ---
@app.route("/api/products", methods=["GET"])
def products():
    if "max_price" in request.args:
        try:
            max_price = float(request.args.get("max_price"))
            
            if math.isnan(max_price) or math.isinf(max_price) or max_price < 0:
                return jsonify({"error": "invalid max_price"}), 400
                
        except ValueError:
            return jsonify({"error": "invalid max_price"}), 400
            
        filtered = [p for p in PRODUCTS if p["cena"] <= max_price]
        return jsonify(filtered)
        
    return jsonify(PRODUCTS)

@app.route("/api/products/<int:product_id>", methods=["GET"])
def product(product_id):
    item = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if item is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(item)

@app.route("/api/products", methods=["POST"])
def add_product():
    data = request.get_json()
    new_id = max((p["id"] for p in PRODUCTS), default=0) + 1
    data["id"] = new_id
    PRODUCTS.append(data)
    return jsonify(data), 201

if __name__ == "__main__":
    app.run(debug=True)