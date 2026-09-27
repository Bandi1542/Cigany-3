import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

@app.route('/generalas', methods=['POST'])
def generate():
    if not client:
        return jsonify({"success": False, "error": "Hiányzó API kulcs a szerveren!"}), 500

    data = request.json or {}
    focim = data.get('focim', '')
    alcim = data.get('alcim', '')

    prompt = f"""
    Készíts egy profi prezentációs dia tartalmát magyarul!
    Prezentáció főcíme: {focim}
    Dia alcíme: {alcim}

    Követelmények:
    - Írj 3 konkrét, szakmailag pontos, lényegre törő pontot a témáról!
    - NE használj általános sablonmondatokat!
    - Formátum: Csak a 3 pontot írd le, mindegyik kezdődjön '• ' karakterrel.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return jsonify({"success": True, "text": response.text.strip()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
