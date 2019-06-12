from favorite_things import app
from api import app as ap

ap.run()

if __name__ == '__main__':
  app.run(debug=True)