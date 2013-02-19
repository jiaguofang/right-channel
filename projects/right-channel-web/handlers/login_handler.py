# -*- coding: utf-8 -*-
'''
Created on Feb 7, 2013

@author: Fang Jiaguo
'''
from handlers.base_handler import BaseHandler, authenticated_async
from settings import collections
from util import encrypt
import tornado.gen
import tornado.web

class LoginHandler(BaseHandler):
    def initialize(self):
        super(LoginHandler, self).initialize()
        self.params['site_nav'] = 'login'

    @authenticated_async()
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        self.render('account/login_page.html')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        email = self.get_argument('email', '').strip()
        password = self.get_argument('password', '')
        persistent_login = self.get_argument('persistent-login', 'false')

        # here we only validate the upper bound and do not use
        # regex to validate email in case regex itself changes
        if (len(email) <= 254 and len(password) <= 16):
            try:
                response, error = yield tornado.gen.Task(collections['accounts'].find_one,
                                                         {'email': email, 'password': encrypt(password)},
                                                         fields={'email': 1})
            except:
                raise tornado.web.HTTPError(500)

            if 'error' in error and error['error']:
                raise tornado.web.HTTPError(500)

            user = response[0]
            if user:
                if persistent_login == 'true':
                    self.set_secure_cookie('email', user['email'])  # Persistent cookie
                else:
                    self.set_secure_cookie('email', user['email'], expires_days=None)  # Session cookie
                next_page = self.get_secure_cookie('next')
                if next_page:
                    self.clear_cookie('next')  # !important
                    self.redirect(next_page)
                else:
                    self.redirect('/')
            else:
                self.params['op_result'] = {'type': 'error', 'message': '您输入的邮箱或密码不正确，请重新输入'}
                self.render('account/login_page.html')
        else:
            raise tornado.web.HTTPError(403)
