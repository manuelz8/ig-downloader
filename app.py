from flask import Flask, render_template, request
import instagram as ig

app = Flask(__name__)

@app.route('/')
def instagram_media():
    return render_template('instagramMedia.html')

@app.route('/get_instagram_media', methods = ['GET', 'POST'])
def get_instagram_content():
    try:
        data = request.get_json()

        url = data.get("url")
        file_directory = ig.get_instagram_media(url)
        response = { 'file_directory': file_directory }
        if 'Fail' in file_directory:
            return response, 400

        return response, 200

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
