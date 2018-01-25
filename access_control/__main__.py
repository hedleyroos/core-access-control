# TODO Fix, imports currently fail when runninig python -m access_control.
from .views import app

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
