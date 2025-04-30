from website import create_app

app = create_app()

if __name__ == "__main__":
    # Run in debug mode for development with auto-reload
    # Use a different port than the mainProgram
    app.run(debug=True, host='0.0.0.0', port=5003) 