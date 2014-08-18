#!/bin/sh

### BEGIN INIT INFO
# Provides:          uwsgi
# Required-Start:    $all
# Required-Stop:     $all
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: starts the uwsgi app server
# Description:       starts uwsgi app server using start-stop-daemon
### END INIT INFO

PATH=/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/local/bin/uwsgi

OWNER=www-data

NAME=uwsgi
DESC=uwsgi

test -x $DAEMON || exit 0

# Include uwsgi defaults if available
if [ -f /etc/default/uwsgi ] ; then
        . /etc/default/uwsgi
fi

set -e

DAEMON_OPTS="--emperor /etc/uwsgi/apps-enabled --daemonize /var/log/uwsgi.log --uid www-data --gid www-data --master --touch-reload=/var/run/uwsgi"

case "$1" in
    start)
        echo -n "Starting $DESC: "
        start-stop-daemon --start --chuid $OWNER:$OWNER --user $OWNER \
            --exec $DAEMON -- $DAEMON_OPTS
        echo "$NAME."
        ;;
    stop)
        echo -n "Stopping $DESC: "
        start-stop-daemon --signal 3 --user $OWNER --quiet --retry 2 --stop \
            --exec $DAEMON
        echo "$NAME."
        ;;
    reload)
        killall -1 $DAEMON
        ;;
    force-reload)
        killall -15 $DAEMON
        ;;
    restart)
        echo -n "Restarting $DESC: "
        start-stop-daemon --signal 3 --user $OWNER --quiet --retry 2 --stop \
            --exec $DAEMON
        sleep 1
        start-stop-daemon --user $OWNER --start --quiet --chuid $OWNER:$OWNER \
            --exec $DAEMON -- $DAEMON_OPTS
        echo "$NAME."
        ;;
    status)
        killall -10 $DAEMON
        ;;
    *)
        N=/etc/init.d/$NAME
        echo "Usage: $N {start|stop|restart|reload|force-reload|status}" >&2
        exit 1
        ;;
esac
exit 0
