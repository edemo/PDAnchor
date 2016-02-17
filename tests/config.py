
excAnswer = "<exception>{0}<trace>{1}</trace></exception>"
cryptoserver_host = "localhost"
cryptoserver_port = 9999
pkcs11lib = "/usr/lib/softhsm/libsofthsm.so" 
#the index of the key in the token
tokenObjectIndex = 1
#index of the slot of the token
tokenSlot = 0
#the correct signature for the data '17203133959'
testHash = '0cb5dbba57d0b9e39243d94f6e205b44f00474c2d83ea5c7b94441e8c29606b43696f7e0d1384be1e2dd258f498d3897746168adf5e4b8eb49b34a4d45548e29'
testSignature = '14d8a8124456c6310c3d8d2ce96ac473f10377def01a7bf6ff1375550d94d5c7d17338d1635fb564bed4df1c82797ea28d1135363b22b16453a0302c77c9a08fcdcf423b732555c5623a90ddb27f3b13f4da4d1ba48e144b5849198847d31096604234190bbc6e1f0b6bb4b1578fcade9f21672d0ed65d9c992f5a68dba033aa4845e54489591fa06d5ee98177e863491cb30a03f06e62e4b9f0f9fe94ee36ca1eb9aaab48b0de592125cdf92280fdb091474e109a1ae1a3da200b97c3dc22a3b501d76f4ee131f70d38f2dca452c76cedc2c1a086eaa78465dbae20f117e107287c02d99f381119a8817d7e4e3c05ecad4dff936d045a122c099bc045c02231'
PIN = "0000"
if False:
    pkcs11lib = "/usr/lib/opensc-pkcs11.so"
    tokenObjectIndex = 0
    tokenSlot = 1
    testSignature = "64cf9bcadfefa3a3d9dd909a521ad1edacdeac5942a91d15e2f53e5e288621725cfe41bbaae277e6d953feb6c08412c5907a904bcce15d70292a4418664b1f50"
