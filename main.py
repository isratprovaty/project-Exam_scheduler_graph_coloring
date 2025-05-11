from app import app  # noqa: F401

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
