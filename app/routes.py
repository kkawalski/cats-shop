from app import app


@app.route("/index", methods=["GET"])
def index():
    return "HELLO WORLD!"
