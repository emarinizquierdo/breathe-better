import csv
import json
import logging
import urllib2
import datetime
import json
import webapp2
import model
import server.seed

class Pollution:

  def __init__(self, id, parameter, tecnic, period, ce01, ce02, ce03, station, timestamp, value):
    self.id = id
    self.parameter = parameter
    self.tecnic = tecnic
    self.period = period
    self.ce01 = ce01
    self.ce02 = ce02
    self.ce03 = ce03
    self.station = station
    self.timestamp = timestamp
    self.value = value


class Stations:

  def __init__(self):
    self.url = "http://www.mambiente.munimadrid.es/opendata/horario.txt"
    self.fieldnames = ( "ce01","ce02","ce03","parameter","tecnic","period","year","month","day",
                        "hour0","v","hour1","v","hour2","v","hour3","v","hour4","v", "hour5","v",
                        "hour6","v","hour7","v","hour8","v","hour9","v","hour10","v","hour11","v",
                        "hour12","v","hour13","v","hour14","v","hour15","v","hour16","v", "hour17",
                        "v","hour18","v","hour19","v","hour20","v","hour21","v","hour22","v","hour23","v")

  def get(self):
    response = urllib2.urlopen(self.url)
    rows = csv.DictReader( response, self.fieldnames)
    for row in rows:
        hour = datetime.datetime.now().hour - 1
        stcode = int(str(row["ce01"]) + str(row["ce02"]) + str(row["ce03"]))
        station = server.seed.Station.query(server.seed.Station.StationCod==stcode).get()
        if station:
            model.UpdateAire(  '' + row["ce01"] + row["ce02"] + row["ce03"] + row["parameter"] + row["year"] + row["month"] + row["day"] + str(hour),
                                datetime.datetime(int(row["year"]), int(row["month"]), int(row["day"]), hour, 0),
                                int(row["parameter"]),
                                int(row["tecnic"]),
                                int(row["period"]),
                                float(row["hour" + str(hour)]),
                                int(row["ce01"]),
                                int(row["ce02"]),
                                int(row["ce03"]),
                                station
                                )


stations = Stations()

class RestHandler(webapp2.RequestHandler):

  def dispatch(self):
    #time.sleep(1)
    super(RestHandler, self).dispatch()


  def SendJson(self, r):
    self.response.headers['content-type'] = 'text/plain'
    self.response.write(json.dumps(r))
    

class LaunchCron(RestHandler):

  def get(self):
    stations.get()

STATIONS = webapp2.WSGIApplication([
    ('/tasks/stations', LaunchCron)
    #('/rest/insert', InsertHandler),
    #('/rest/delete', DeleteHandler),
    #('/rest/update', UpdateHandler),
], debug=True)