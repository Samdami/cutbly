from pipcut import app, db

if __name__ == "__main__":
    # Ensure tables exist before running (no debug to avoid debugger noise)
    with app.app_context():
        db.create_all()
    app.run()
