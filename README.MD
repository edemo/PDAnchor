PDAnchor

This is the trust anchor for an anonymous assured identity provider.
We have a smart card with a private key known by no one.
Anyone can submit a personal identity number ("személyi szám",
it is a unique identifier for Hungarian citizens), along with a string
representing mother's name and gets
the hash of the signature of the identity number.

This gives us a basic service, which helps us to make sure we have
people only once in our voter database, without having to know
anything about our voters.

To avoid brute force and Denial of Service attacks,
one IP can query the database only once in a minute.


installation notes:

dependencies include:

 - python
 - apache2
 - python-crypto
 - opensc
 - libapache-mod-wsgi
 - softhsm (only for testing)

See Makefile  and the testserver directory for hints

