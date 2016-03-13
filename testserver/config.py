# pylint: disable=invalid-name
cryptoserver_host = "localhost"
cryptoserver_port = 9999
inputlength = 256
outputlength = 256
excAnswer = "<exception>{0}<trace>{1}</trace></exception>"
minimum_time = 0
pkcs11lib = "/usr/lib/softhsm/libsofthsm.so"
#the index of the key in the token
tokenObjectIndex = 1
#index of the slot of the token
tokenSlot = 0
#the correct signature for the data '17203133959'
testHash = '64cf9bcadfefa3a3d9dd909a521ad1edacdeac5942a91d15e2f53e5e288621725cfe41bbaae277e6d953feb6c08412c5907a904bcce15d70292a4418664b1f50'
testSignature = '8d6359fbda9c239fdb43680f4aa4d8a8f4f31fe119eec07ec3b514eed5a4148c7f585aec0a58b9f3cb9c254651196d11d9dbf866ad91250cf7670902c5f693082f5938cc2e3c6584708cdc08b03fe5e601306f0835644d4fe916923965b5db1772fbae50399520c530c5ac989c7d91f3b916c8a1ed058cdad09ed854981e32e50a1c47670e294983f9c0d333ec62afbdeea12c403a346f539e63074e9a976eb483cccbb32a4d959ca1763a25bba405e407952a78888ab64cd139f9b3c860d7ce7750455647bd40481f9019cbe5d139f2f50f958aa6300870652f0cba6b38f9104f795dae5dd091aacb9be2def7aaf30f7a14facc0e7f4908761090b5867f3ef1'
PIN = "0000"
if False:
    pkcs11lib = "/usr/lib/opensc-pkcs11.so"
    tokenObjectIndex = 0
    tokenSlot = 1
    testSignature = "64cf9bcadfefa3a3d9dd909a521ad1edacdeac5942a91d15e2f53e5e288621725cfe41bbaae277e6d953feb6c08412c5907a904bcce15d70292a4418664b1f50"
