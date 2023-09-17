from app import app
# from File_Uploader import app
app.secret_key = 'actual changed it 56902-3-5g'  # Change this!


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=80, debug=True)
    app.run()