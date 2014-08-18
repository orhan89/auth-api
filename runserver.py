import os
import APP_NAME

if __name__ == '__main__':
    APP_NAME.configure_app('/etc/APP_NAME/development.cfg')
    APP_NAME.app.run(host='0.0.0.0', port=5000)
