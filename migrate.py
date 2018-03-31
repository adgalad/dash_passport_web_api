
import json
from App import app, api, address
from models.db import db
from models.User import *
from models.Permission import *


if __name__ == '__main__':
  db.create_all()


  permissions = list(map(lambda n: Permission(name=n), ["canStamp", "canActivate", "canRecharge"]))
  for permission in permissions:
    db.session.add(permission)

  groups = { "Admin": permissions
           , "Participant": []
           , "Staff": permissions
           }

  for name, permissions in groups.items():
    db.session.add(Group(name = name, permissions = permissions))




  db.session.commit()
