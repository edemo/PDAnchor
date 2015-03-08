PDAnchor

This is the trust anchor for an anonymous assured identity provider.
We have a smart card with a private key known by no one.
Anyone can submit a personal identity number ("személyi szám",
it is a unique identifier for Hungarian citizens), and gets
the md5 hash of the signature of the identity number.

This gives us a basic service, which helps us to make sure we have
people only once in our voter database, without having to know
anything about our voters.

To avoid brute force and Denial of Service attacks,
one IP can query the database only once in a minute.


installation notes:

- this program is single-threaded. limit apache to one threads. use

    StartServers 1
    ServerLimit 1
    ThreadLimit 1

- map wsgi/app.fcgi to /anchor. if you git cloned to /usr/local/PDAnchor , use this:

        WSGIScriptAlias /anchor /usr/local/PDAnchor/wsgi/app.fcgi
        <Directory /usr/local/PDAnchor/wsgi>
            Require all granted
        </Directory>

