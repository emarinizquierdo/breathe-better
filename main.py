import json
import webapp2
import time

import model
import server.seed
import logging

logging.info('Main')


def AsDict(aire):
  return {'id': aire.key.id(), 'timestamp' : str(aire.timestamp), 'parameter' : aire.parameter, 'tecnic' : aire.tecnic,
          'period' : aire.period, 'value' : aire.value, 'ce01' : aire.ce01, 'ce02' : aire.ce02, 'ce03' : aire.ce03, 
          'stationObject' : { 'Latitud_D' : aire.station.Latitud_D, 'Longitud_D' : aire.station.Longitud_D} }


class RestHandler(webapp2.RequestHandler):

  def dispatch(self):
    #time.sleep(1)
    super(RestHandler, self).dispatch()


  def SendJson(self, r):
    self.response.headers['content-type'] = 'text/plain'
    self.response.write(json.dumps(r))
    

class QueryHandler(RestHandler):

  def get(self):
    parameter = self.request.get('parameter')
    year = self.request.get('year', default_value=2015)
    month = self.request.get('month', default_value=1)
    day = self.request.get('day', default_value=1)
    hour = self.request.get('hour', default_value=1)
    aires = model.AllAire(parameter, year, month, day, hour)
    r = [ AsDict(aire) for aire in aires ]
    self.SendJson(r)


class UpdateHandler(RestHandler):

  def post(self):
    r = json.loads(self.request.body)
    guest = model.UpdateGuest(r['id'], r['first'], r['last'])
    r = AsDict(guest)
    self.SendJson(r)


class InsertHandler(RestHandler):

  def post(self):
    r = json.loads(self.request.body)
    guest = model.InsertGuest(r['first'], r['last'])
    r = AsDict(guest)
    self.SendJson(r)


class DeleteHandler(RestHandler):

  def post(self):
    r = json.loads(self.request.body)
    model.DeleteGuest(r['id'])

class SeedHandler(RestHandler):

  def get(self):
    seed = server.seed.Inflate()

APP = webapp2.WSGIApplication([
    ('/api/aires', QueryHandler),
    ('/seed', SeedHandler)
    #('/rest/insert', InsertHandler),
    #('/rest/delete', DeleteHandler),
    #('/rest/update', UpdateHandler),
], debug=True)


