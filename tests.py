#!/usr/bin/env python
from coverage import coverage
import os
import unittest
from app import create_app, db
from app.models import User
from config import Config, basedir

cov = coverage(branch=True, omit=['venv/*', 'tests.py'])
cov.start()


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


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

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_activating_user(self):
        u = User(username='susan')
        db.session.add(u)
        db.session.commit()
        token = u.get_activate_token()
        User.activate_user(token)
        self.assertTrue(u.is_active)


if __name__ == '__main__':
    try:
        unittest.main(verbosity=2)
    except:
        pass
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    print("\nHTML version: " + os.path.join(basedir, "tmp/coverage/index.html"))
    cov.html_report(directory='tmp/coverage')
    cov.erase()
