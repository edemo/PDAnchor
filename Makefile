all: hu.po test killserver

test: runcryptoserver runserver
	./runtests.sh

runserver: restartsyslog runcryptoserver
	mkdir -p tmp; apache2 -X -f $$(pwd)/testserver/apache2.conf &

restartsyslog:
	cp testserver/syslog-ng.conf /etc/syslog-ng/syslog-ng.conf
	service syslog-ng restart
	cat /dev/xconsole&

killserver: stopcryptoserver
	kill $$(cat tmp/httpd_anchor.pid)

clean:
	rm -rf tmp

runcryptoserver: preparesofthsm
	/sbin/start-stop-daemon --start --background  --pidfile  /tmp/cryptoserver.pid --make-pidfile -d $(CURDIR) --exec cryptoserver/cryptoserver.py -- -H 0.0.0.0 --module /usr/lib/softhsm/libsofthsm2.so -d d34db33f;sleep 2

preparesofthsm:
	tools/preparesofthsm

stopcryptoserver:
	/sbin/start-stop-daemon --stop --pidfile  /tmp/cryptoserver.pid

testenv:
	docker run --rm -p 8890:8890 -p 9999:9999 -w /PDAnchor -v $$(pwd):/PDAnchor -it edemo/pdoauth:latest

messages.po: $(wildcard src/*.py) $(wildcard cryptoserver/*.py)
	xgettext -L Python -j --package-name=PDAnchor src/*.py cryptoserver/*.py

hu.po: messages.po
	msgmerge -U hu.po messages.po

