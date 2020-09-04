from app import create_app
from decouple import config

app = create_app()

if __name__ == '__main__':
    app.run(debug=config('DEBUG'), host='0.0.0.0', port=5700)
