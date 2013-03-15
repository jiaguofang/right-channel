'''
Created on Mar 13, 2013

@author: Fang Jiaguo
'''
from bson.objectid import ObjectId
from settings import mongodb
from tornado.web import HTTPError
import tornado.gen
import tornado.web

class MovieToWatchHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        email = self.get_secure_cookie('email')
        if email:
            # 400 Bad Request if id not provided
            movie_id = self.get_argument('id')

            # get movie information from movies collection
            try:
                response, error = yield tornado.gen.Task(mongodb['movies'].find_one,
                                                         {'_id': ObjectId(movie_id)},
                                                         fields={'title': 1, 'original_title': 1, 'year': 1})
            except:
                raise tornado.web.HTTPError(500)

            if error.get('error'):
                raise tornado.web.HTTPError(500)

            if response[0]:
                movie = response[0]
                movie['id'] = movie.pop('_id')
            else:
                raise tornado.web.HTTPError(400)  # Bad Request

            # add movie to to_watch list in accounts collection
            try:
                response, error = yield tornado.gen.Task(mongodb['accounts'].update,
                                                         {'email': email},
                                                         {'$addToSet': {'to_watch.movie': movie}})
            except:
                raise tornado.web.HTTPError(500)

            if error.get('error'):
                raise tornado.web.HTTPError(500)

            self.finish()
        else:
            raise HTTPError(401)  # Unauthorized
