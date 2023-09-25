from flask import Flask, render_template, request
import instagram as ig

app = Flask(__name__)
app.config['TIMEOUT'] = 50

@app.route('/')
def instagram_media():
    return render_template('instagramMedia.html')

@app.route('/get_instagram_media', methods = ['GET', 'POST'])
def get_instagram_content():
    try:
        data = request.get_json()

        url = data.get("url")
        content_data = ig.get_instagram_media(url)

        if content_data['success'] == False:
            return content_data, 400

        audit_data = {
            'username': content_data['username'],
            'media_url': content_data['media_url'],
            'followers': content_data['followers'],
        }
        ig.instagram_audit(audit_data)

        return content_data, 200

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
