import os
import unittest
import AuthAPI

class AuthAPITest(unittest.TestCase):

    def cleanDatabase(self):
        # connect to db
        d = AuthAPI.app.config['DB_DATABASE']
        u = AuthAPI.app.config['DB_USERNAME']
        p = AuthAPI.app.config['DB_PASSWORD']
        f = "db/AuthAPI-api-test.sql"

        from subprocess import Popen, PIPE
        process = Popen('mysql -u%s -p%s' % (u, p),
                        stdout=PIPE, stdin=PIPE, shell=True)
        output = process.communicate('source ' + f)[0]
        print output

    def populateDatabase(self):
        # connect to db
        d = AuthAPI.app.config['DB_DATABASE']
        u = AuthAPI.app.config['DB_USERNAME']
        p = AuthAPI.app.config['DB_PASSWORD']
        f = "db/AuthAPI-data-test.sql"

        from subprocess import Popen, PIPE
        process = Popen('mysql %s -u%s -p%s' % (d, u, p),
                        stdout=PIPE, stdin=PIPE, shell=True)
        output = process.communicate('source ' + f)[0]
        print output

    def setUp(self):
        AuthAPI.configure_app('/etc/AuthAPI/testing.cfg')
        self.app = AuthAPI.app.test_client()
        self.cleanDatabase()
        self.populateDatabase()
        print "++++++++++++++++++"

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
    print "Closing..."
