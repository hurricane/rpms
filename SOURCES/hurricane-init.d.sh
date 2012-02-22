#! /bin/bash
### BEGIN INIT INFO
# Provides:          hurricane
# Required-Start:    $all
# Required-Stop:     $all
# Default-Start:
# Default-Stop:      0 1 6
# Short-Description: Starts hurricane
# chkconfig: - 80 15
# Description: hurricane
### END INIT INFO

# Source function library.
. /etc/rc.d/init.d/functions

# Pull in sysconfig settings
[ -f /etc/sysconfig/hurricane ] && . /etc/sysconfig/hurricane

DAEMON=/usr/bin/hurricane
DAEMON_OPTS=$HURRICANE_CONFIG
NAME=hurricane
PID_FILE=${PIDFILE:-/var/run/${NAME}/${NAME}.pid}
LOCK_FILE=${LOCKFILE:-/var/lock/subsys/${NAME}}

start() {
    echo -n $"Starting ${NAME}: "
    daemon --pidfile=${PID_FILE} --user $NAME\
        $DAEMON $DAEMON_OPTS
    RETVAL=$?
    echo
    [ $RETVAL -eq 0 ] && touch $LOCK_FILE
    return $RETVAL
}

stop() {
    echo -n $"Stopping ${NAME}: "
    killproc -p ${PID_FILE} -d 10 $DAEMON
    RETVAL=$?
    echo
    [ $RETVAL = 0 ] && rm -f ${LOCK_FILE} ${PID_FILE}
    return $RETVAL
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
        status -p ${PID_FILE} $DAEMON
        RETVAL=$?
        ;;
    restart|force-reload)
        stop
        start
        ;;
    *)
        N=/etc/init.d/${NAME}
        echo "Usage: $N {start|stop|restart|force-reload}" >&2
        RETVAL=2
        ;;
esac

exit $RETVAL
