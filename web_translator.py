from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
import threading

app = Flask(__name__)

# 번역 함수
def translate_text(text, target_lang):
    try:
        translator = GoogleTranslator(source_language='auto', target_language=target_lang)
        result = translator.translate(text)
        return result
    except Exception as e:
        return f"번역 오류: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data.get('text', '').strip()
    target_lang = data.get('target_lang', 'en')

    if not text:
        return jsonify({'error': '번역할 텍스트를 입력해주세요.'})

    # 비동기로 번역 실행
    result = translate_text(text, target_lang)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)