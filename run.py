from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)  # Cambia el puerto a 8080 o cualquier otro puerto disponible