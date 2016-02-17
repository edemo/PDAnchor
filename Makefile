all: test killserver

test: runcryptoserver runserver
	./runtests.sh

runserver: runcryptoserver
	mkdir -p tmp;SOFTHSM_CONF=testserver/softhsm.conf apache2 -X -f $$(pwd)/testserver/apache2.conf &

killserver: stopcryptoserver
	kill $$(cat tmp/httpd_anchor.pid)

clean:
	rm -rf tmp

runcryptoserver:
	/sbin/start-stop-daemon --start --background  --pidfile  /tmp/cryptoserver.pid --make-pidfile -d $(PWD) --exec cryptoserver/cryptoserver.py -- --module /usr/lib/softhsm/libsofthsm.so -d d34db33f -e SOFTHSM_CONF=tests/softhsm.conf;sleep 2

stopcryptoserver:
	/sbin/start-stop-daemon --stop --pidfile  /tmp/cryptoserver.pid

