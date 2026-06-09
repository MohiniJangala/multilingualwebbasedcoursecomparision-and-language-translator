from flask import Flask, render_template, send_from_directory
from routes.translate import translate_bp
import os
app = Flask(__name__)
# Register blueprint
app.register_blueprint(translate_bp)
# Home route (index page)
@app.route('/')
def home():
    return render_template('index.html')
#  Serve output videos (imp)
@app.route('/output/<path:filename>')
def serve_video(filename):
    return send_from_directory('output/final_videos', filename)
#  serve uploaded files
@app.route('/static/uploads/<path:filename>')
def serve_uploads(filename):
    return send_from_directory('static/uploads', filename)
if __name__ == '__main__':
    # run app (stable mode for your project)
    app.run(debug=False, threaded=True,port=5001)
