from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        debug=True,
        port=8080,
        host="localhost",
        threaded=True,
        use_reloader=True,
        load_dotenv=True,
    )
