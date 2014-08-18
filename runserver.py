import os
import AuthAPI

if __name__ == '__main__':
    AuthAPI.configure_app('/etc/AuthAPI/development.cfg')
    AuthAPI.app.run(host='0.0.0.0', port=5000)
