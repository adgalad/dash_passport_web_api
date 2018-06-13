
from models.db import db
from models.User import *
from models.Passport import *
from models.Permission import *
from models.Event import *
from models.Vendor import *
from controller.Event import createEvent
import datetime
from datetime import date
from sqlalchemy import event as sqlevent
from sqlalchemy import DDL

if __name__ == '__main__':
  db.create_all()


  staffPerms = list(map(lambda n: Permission(name=n), ["canStamp", "canActivate", "canRecharge"]))
  participantPerms = list(map(lambda n: Permission(name=n), ["canSeePassport"]))
  allPerms = staffPerms + participantPerms

  for permission in allPerms:
    db.session.add(permission)

  groups = { "Admin": allPerms
           , "Participant": participantPerms
           , "Staff": staffPerms
           , "Vendor": staffPerms
           }

  for name, permissions in groups.items():
    db.session.add(Group(name = name, permissions = permissions))

  admin = User( id="1", email="admin@dash.com",
                firstName="__admin__", lastName="__admin__", active=True)
  admin.hash_password("carlos2533")
  group = Group.query.filter_by(name="Admin").first()
  group.users.append(admin)

  event = createEvent(name="Dash Maracay", date=date(2018,5,24), location="Maracay", duff_value=0.012, active=True)
  db.session.add(event)
  db.session.add(admin)
  db.session.commit()
  vendors = list(map(lambda n: Vendor(name=n, events=[event], user=admin),
               [ "Guarapita El Gran Varón"
               , "BurgerManía"
               , "Woufles"
               , "Cocotento"
               , "Chiringuitos"
               , "Cerveza Viking Sur"
               , "Pixie Liquors"
               , "Restaurante Viejo Puente"
               , "Be Nuts"
               , "Chocolate Digatti" ]))
  for v in vendors:
    db.session.add(v)

  foundations = list(map(lambda n: Vendor(name=n, isFoundation=True, user=admin, events=[event]),
               [ "Operacion Sonrisa", "Fundameste" ]))
  for f in foundations:
    db.session.add(f)

  db.session.add(Product(vendor=vendors[0], name="Harina Pan", price=0.05))
  db.session.add(Product(vendor=vendors[0], name="Cerveza", price=0.05))

  
  db.session.commit()



# this.items = 
