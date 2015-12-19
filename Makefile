all: tests

tests:
	./runtests

runserver:
	mkdir -p tmp;SOFTHSM_CONF=tests/softhsm.conf apache2 -X -f $$(pwd)/apache2.conf &

killserver:
	kill $$(cat tmp/httpd_anchor.pid)

clean:
	rm -rf tmp
