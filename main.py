
from App import app, api, address
from models.db import db
import models.Passport 
import controller.User



if __name__ == '__main__':
  db.create_all()
  app.run(debug=True,host=address, port=5001)
