import os
import unittest
import APP_NAME

class APP_NAMETest(unittest.TestCase):

    def cleanDatabase(self):
        # connect to db
        d = APP_NAME.app.config['DB_DATABASE']
        u = APP_NAME.app.config['DB_USERNAME']
        p = APP_NAME.app.config['DB_PASSWORD']
        f = "db/APP_NAME-api-test.sql"

        from subprocess import Popen, PIPE
        process = Popen('mysql -u%s -p%s' % (u, p),
                        stdout=PIPE, stdin=PIPE, shell=True)
        output = process.communicate('source ' + f)[0]
        print output

    def populateDatabase(self):
        # connect to db
        d = APP_NAME.app.config['DB_DATABASE']
        u = APP_NAME.app.config['DB_USERNAME']
        p = APP_NAME.app.config['DB_PASSWORD']
        f = "db/APP_NAME-data-test.sql"

        from subprocess import Popen, PIPE
        process = Popen('mysql %s -u%s -p%s' % (d, u, p),
                        stdout=PIPE, stdin=PIPE, shell=True)
        output = process.communicate('source ' + f)[0]
        print output

    def setUp(self):
        APP_NAME.configure_app('/etc/APP_NAME/testing.cfg')
        self.app = APP_NAME.app.test_client()
        self.cleanDatabase()
        self.populateDatabase()
        print "++++++++++++++++++"

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
    print "Closing..."
