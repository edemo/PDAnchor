
excAnswer = "<exception>{0}<trace>{1}</trace></exception>"
cryptoserver_host = "localhost"
cryptoserver_port = 9999
outputlength = 256
inputlength = 256
pkcs11lib = "/usr/lib/softhsm/libsofthsm2.so" 
#the index of the key in the token
tokenObjectIndex = 1
#index of the slot of the token
tokenSlot = 0
#the correct signature for the data '17203133959'
testHash = 'd1785ee7e714ea7c8515bdd8e19d72551d284e7c2f36741684b35ca505174067aa56fca935a30c303b6c47310fc16c0e9b286226d622f047be49a90e3734486a'
testSignature = '7c671d8109230cfe31fbfe1a99f7c6d4393a7d454ce7faadce2c07a05da4f8f08501ea4f2b656a737c726444b52f08503225077067613f14625771033a3767a1d1d51beb53b65eb184a440053388c63e14713c0624f75473382e818ca78816900d8edac34664808b90a161e975260a2cd0f062dd263194d736c62707b468beff5ffee6a30a7562a85bcd97508f44e451f5536256410a28fea7b4f85295077a3645b93c042ef8664cbebf31848d1ca5285cfb0dd74ec23702d3f8e6c6d22daee5e2b72ddda1b336e83b5831ee016e57cb0c3f0ceec1b1d297675993e961028de33b53ceadcbee24786a8b231c0bf7b39df95c3ac2b12d07a4d0aeb4db368f6c70'

PIN = "0000"
if False:
    pkcs11lib = "/usr/lib/opensc-pkcs11.so"
    tokenObjectIndex = 0
    tokenSlot = 1
    testSignature = "64cf9bcadfefa3a3d9dd909a521ad1edacdeac5942a91d15e2f53e5e288621725cfe41bbaae277e6d953feb6c08412c5907a904bcce15d70292a4418664b1f50"
