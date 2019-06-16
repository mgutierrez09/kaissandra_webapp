# -*- coding: utf-8 -*-
"""
Created on Sat May 11 17:57:32 2019

@author: mgutierrez
"""

import unittest
import os
from config import Config
from app import create_app, db
from app.tables import User, Trader

class TestConfig(Config):
    TESTING = True
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite://'#+ os.path.join(basedir, 'apptest.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_tests(self):
        self.assertFalse(False)
        
    def test_add2db(self):
        """  """
        data = {'username':'test',
                'email':'test@example.com',
                'password':'thisisapassword'
                }
        user = User()
        self.assertEqual(user.add2db(data), 1)
        
        
        data = {'nofield':'test',
                'email':'test@example.com',
                'password':'thisisapassword'
                }
        user = User()
        self.assertEqual(user.add2db(data), -1)
        
        
    def test_validate_fields(self):
        data = {'username':'test2',
                'email':'test2@example.com',
                'password':'thisisapassword'
                }
        user = User()
        self.assertEqual(user.validate_fields(data), 1)
        
        data = {'email':'test@example.com',
                'password':'thisisapassword'
                }
        user = User()
        self.assertEqual(user.validate_fields(data), -1)
        
        data = {'username':'test',
                'email':'tes2example.com',
                'password':'short'
                }
        user = User()
        self.assertEqual(user.validate_fields(data), -3)
        
        data = {'username':'test2',
                'email':'tes2t@example.com',
                'password':'short'
                }
        user = User()
        self.assertEqual(user.validate_fields(data), -4)
        
    def test_validate_fields_and_add2db(self):
        """  """
        data = {'username':'test',
                'email':'test@example.com',
                'password':'thisisapassword'
                }
        user = User()
        self.assertEqual(user.add2db(data), 1)
        
        
        data = {'nofield':'test',
                'email':'test@example.com',
                'password':'thisisapassword'
                }
        user = User()
        self.assertEqual(user.add2db(data), -1)
        
        data = {'username':'test',
                'email':'test@example.com',
                'password':'short'
                }
        user = User()
        self.assertEqual(user.validate_fields(data), -2)
        
        data = {'username':'test2',
                'email':'test@example.com',
                'password':'short'
                }
        user = User()
        self.assertEqual(user.validate_fields(data), -3)
        
    def test_to_dict(self):
        self.assertFalse(False)
        
class TraderModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_tests(self):
        self.assertFalse(False)
        
    def test_add2db(self):
        """  """
        data = {'tradername':'tradername',
                }
        trader = Trader()
        self.assertEqual(trader.add2db(data), 1)
        
    def test_validate_fields(self):
        data = {'tradername':'tradername',
                }
        trader = Trader()
        self.assertEqual(trader.validate_fields(data), 1)
        
        data = {'email':'test@example.com',
                }
        trader = Trader()
        self.assertEqual(trader.validate_fields(data), -1)
        
        
    def test_validate_fields_and_add2db(self):
        """  """
        data = {'tradername':'tradername',
                }
        trader = Trader()
        trader.add2db(data)        
        
        data = {'nofield':'test',
                }
        trader = Trader()
        self.assertEqual(trader.add2db(data), -1)
        
        data = {'tradername':'tradername',
                }
        trader = Trader()
        self.assertEqual(trader.validate_fields(data), -2)
        
        
    def test_to_dict(self):
        self.assertFalse(False)
    
    
if __name__ == '__main__':
    unittest.main(verbosity=2)