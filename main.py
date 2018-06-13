
from App import app, address, port
from models.db import db
import controller.Passport 
import controller.Event
import controller.Vendor
import controller.User

from models.Event import *
from models.Passport import *
from models.User import *
from models.Permission import *
from models.Vendor import *


if __name__ == '__main__':
  db.create_all()
  
  admin.add_view(ModelView(Purchase, db.session))
  admin.add_view(ModelView(Product, db.session))
  admin.add_view(ModelView(Vendor, db.session))
  admin.add_view(ModelView(Event, db.session))
  admin.add_view(ModelView(Passport, db.session))
  admin.add_view(ModelView(Group, db.session))
  admin.add_view(ModelView(Permission, db.session))
  admin.add_view(ModelView(User, db.session))

  app.run(debug=True,host="0.0.0.0", port=int(port))
