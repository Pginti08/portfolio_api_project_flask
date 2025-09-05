from flask import Blueprint, request, jsonify
from googletrans import Translator

translate_bp = Blueprint('translate', __name__)
translator = Translator()

@translate_bp.route('/', methods=['POST'])
def translate_content():
    data = request.get_json()
    content = data.get('content', "")
    target_lang = data.get('target_lang', "en")

    if not content:
        return jsonify({"error": "Content is required"}), 400

    try:
        # Use googletrans for real translation
        translation = translator.translate(content, dest=target_lang)
        translated_text = translation.text
        return jsonify({
            "translated_content": translated_text,
            "source_lang": translation.src,
            "target_lang": translation.dest
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
