
excAnswer = "<exception>{0}<trace>{1}</trace></exception>"
#the index of the key in the token
tokenObjectIndex = 0
#index of the slot of the token
tokenSlot = 1
#the correct signature for the data '17203133959'
testSignature = '8800f4a1d480e920e681df9e6a8026f7418dfab6cac74d49c020468327b254d74fee5d7c52893a2bf73c3a48bafc0f34ddd4bae1fbe6aa37159838504fa441069a6b4cd8e8c6269dc099d43f63558831f26f65d1ced0ee11fd775efd9e1fc3f996b3c8584d2e081c0c321e86798f367c9691d88887264ec29a79229702687630'
import sys
from os.path import expanduser
home = expanduser("~")
sys.path.append(expanduser("~/.cardinfo"))
from cardinfo import PIN  # @UnresolvedImport @UnusedImport


