
excAnswer = "<exception>{0}<trace>{1}</trace></exception>"
pkcs11lib = "/usr/lib/softhsm/libsofthsm.so" 
#the index of the key in the token
tokenObjectIndex = 1
#index of the slot of the token
tokenSlot = 0
#the correct signature for the data '17203133959'
testSignature = '8d6359fbda9c239fdb43680f4aa4d8a8f4f31fe119eec07ec3b514eed5a4148c7f585aec0a58b9f3cb9c254651196d11d9dbf866ad91250cf7670902c5f693082f5938cc2e3c6584708cdc08b03fe5e601306f0835644d4fe916923965b5db1772fbae50399520c530c5ac989c7d91f3b916c8a1ed058cdad09ed854981e32e50a1c47670e294983f9c0d333ec62afbdeea12c403a346f539e63074e9a976eb483cccbb32a4d959ca1763a25bba405e407952a78888ab64cd139f9b3c860d7ce7750455647bd40481f9019cbe5d139f2f50f958aa6300870652f0cba6b38f9104f795dae5dd091aacb9be2def7aaf30f7a14facc0e7f4908761090b5867f3ef1'
PIN = "0000"
if False:
    pkcs11lib = "/usr/lib/opensc-pkcs11.so"
    tokenObjectIndex = 0
    tokenSlot = 1
    testSignature = "8800f4a1d480e920e681df9e6a8026f7418dfab6cac74d49c020468327b254d74fee5d7c52893a2bf73c3a48bafc0f34ddd4bae1fbe6aa37159838504fa441069a6b4cd8e8c6269dc099d43f63558831f26f65d1ced0ee11fd775efd9e1fc3f996b3c8584d2e081c0c321e86798f367c9691d88887264ec29a79229702687630"
