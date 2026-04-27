from flask import Flask, request, jsonify, send_file
import google.generativeai as genai
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

# ====================== שנה כאן את ה-API KEY ======================
genai.configure(api_key=AIzaSyCvWGtgzmTdPU90m1R2kcyTDqCS-kWn4Jg)
# =================================================================

@app.route('/gemini', methods=['POST'])
def gemini_webhook():
    try:
        # קבלת נתונים מימות
        recording_url = request.form.get('recording_url') or request.form.get('RecordUrl')
        
        # לעת עתה - שאלה קבועה (בהמשך נוסיף הבנת דיבור)
        user_text = "שלום, ספר לי משהו מעניין"

        # שליחה לגמיני
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(f"ענה בעברית בצורה נעימה: {user_text}")
        
        answer_text = response.text

        # המרה לקול
        tts = gTTS(answer_text, lang='he', slow=False)
        filename = f"answer_{uuid.uuid4().hex[:8]}.mp3"
        tts.save(filename)

        # החזרה לימות
        return jsonify({
            "action": "play",
            "url": f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'localhost')}/{filename}",
            "hangup": "no"
        })

    except Exception as e:
        return jsonify({"action": "play", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"})

# שרת קבצי שמע
@app.route('/<path:filename>')
def serve_file(filename):
    if os.path.exists(filename) and filename.endswith('.mp3'):
        return send_file(filename, mimetype='audio/mpeg')
    return "File not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
