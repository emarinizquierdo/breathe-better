from google.appengine.ext import ndb
import server.seed
import datetime
from datetime import timedelta

class Aire(ndb.Model):
    id = ndb.StringProperty(indexed=False)
    timestamp = ndb.DateTimeProperty()
    parameter = ndb.IntegerProperty()
    tecnic = ndb.IntegerProperty(indexed=False)
    period = ndb.IntegerProperty(indexed=False)
    value = ndb.FloatProperty(indexed=False)
    ce01 = ndb.IntegerProperty(indexed=False)
    ce02 = ndb.IntegerProperty(indexed=False)
    ce03 = ndb.IntegerProperty(indexed=False)
    station = ndb.StructuredProperty(server.seed.Station)

def AllAire(parameters, year, month, day, hour):
    tempTime = datetime.datetime(int(year), int(month), int(day), int(hour), 0)
    return Aire.query(Aire.parameter.IN(parameters), Aire.timestamp == tempTime)

def UpdateAire(id, timestamp, parameter, tecnic, period, value, ce01, ce02, ce03, station):
  aire = Aire(id=id, timestamp=timestamp, parameter=parameter, tecnic=tecnic, period=period, value=value, ce01=ce01, ce02=ce02, ce03=ce03, station=station)
  aire.put()
  return aire

def InsertAire(id, timestamp, parameter, tecnic, period, value, ce01, ce02, ce03):
  aire = Aire(id=id, timestamp=timestamp, parameter=parameter, tecnic=tecnic, period=period, value=value, ce01=ce01, ce02=ce02, ce03=ce03)
  aire.put()
  return aire