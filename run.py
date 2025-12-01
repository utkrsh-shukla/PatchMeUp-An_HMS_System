from app import create_app

app = create_app()

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("Hospital Management System - Development Server")
    print("=" * 60)
    print("\nServer running at: http://localhost:5000")
    print("Press CTRL+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
