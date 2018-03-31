
import json
from App import app, api, address
from models.db import db
import models.Passport 
import controller.User



if __name__ == '__main__':
  # server = json.load(open('config.json'))['flask']
  # User.app.run(debug=True,host=server['network'], port=int(server['port']))
  db.create_all()
  app.run(debug=True,host=address, port=5001)
