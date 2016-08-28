from wscoc_directory import app

@app.route('/')
def index():
    return 'Hello World!'