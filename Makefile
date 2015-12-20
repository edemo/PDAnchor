all: tests

tests:
	./runtests

runserver:
	mkdir -p tmp;SOFTHSM_CONF=testserver/softhsm.conf apache2 -X -f $$(pwd)/testserver/apache2.conf &

killserver:
	kill $$(cat tmp/httpd_anchor.pid)

clean:
	rm -rf tmp
