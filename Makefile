all: hu.po test killserver

test: runcryptoserver runserver
	./runtests.sh

runserver: runcryptoserver
	mkdir -p tmp;SOFTHSM_CONF=testserver/softhsm.conf apache2 -X -f $$(pwd)/testserver/apache2.conf &

killserver: stopcryptoserver
	kill $$(cat tmp/httpd_anchor.pid)

clean:
	rm -rf tmp

runcryptoserver:
	/sbin/start-stop-daemon --start --background  --pidfile  /tmp/cryptoserver.pid --make-pidfile -d $(CURDIR) --exec cryptoserver/cryptoserver.py -- -H 0.0.0.0 --module /usr/lib/softhsm/libsofthsm.so -d d34db33f -e SOFTHSM_CONF=tests/softhsm.conf;sleep 2

stopcryptoserver:
	/sbin/start-stop-daemon --stop --pidfile  /tmp/cryptoserver.pid

testenv:
	docker run --rm -p 8890:8890 -p 9999:9999 -v $$(pwd):/PDAnchor -it magwas/edemotest:master

messages.po: $(wildcard src/*.py) $(wildcard cryptoserver/*.py)
	xgettext -L Python -j --package-name=PDAnchor src/*.py cryptoserver/*.py

hu.po: messages.po
	msgmerge -U hu.po messages.po

