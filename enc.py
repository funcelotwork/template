#import dis
import time
import hashlib
import math
from operator import itemgetter

def frequency(text):
  count = {}
  for key in text:
    count[key] = count[key] + 1 if count.get(key) else 1
  return count

def convert(obj):
  return sorted(list(map(lambda key: [key, obj[key]], obj.keys())), key=itemgetter(0))

def multisort(xs, specs):
  for key, reverse in reversed(specs):
    xs.sort(key=itemgetter(key), reverse=reverse)
  return xs

def sort(array):
  return multisort(list(array), ((1,True), (0, False)))

def chars(text):
  freq = frequency(text)
  items = convert(freq)
  sort_items = sort(items)
  return {
    "char": list(map(itemgetter(0), sort_items)),
    "freq": list(map(itemgetter(1), sort_items))
  }

IV = 1
shift = 1

alphabet = """~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:\"ZXCVBNM<>?`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./ 
"""
sha_alphabet = hashlib.sha3_512(alphabet.encode("utf-8")).hexdigest()
plaintext = """The atmosphere of Mars is about 100 times thinner than Earth's, and it is 95 percent carbon dioxide. Here's a breakdown of its composition, according to a NASA fact sheet:

Carbon dioxide: 95.32 percent
Nitrogen: 2.7 percent
Argon: 1.6 percent
Oxygen: 0.13 percent
Carbon monoxide: 0.08 percent
Also, minor amounts of: water, nitrogen oxide, neon, hydrogen-deuterium-oxygen, krypton and xenon."""
sha_plaintext = hashlib.sha3_512(plaintext.encode("utf-8")).hexdigest()

class prng:
  def __init__(self, seed):
    self._seed = seed % 2147483647
    if self._seed <= 0:
      self._seed += 2147483646

  def next(self, *argv):
    self._seed = (self._seed * 48271) % 2147483647
    length = len(argv)
    if length == 0:
      return self._seed / 2147483647
    elif length == 1:
      a = argv[0]
      return (self._seed / 2147483647) * a
    elif length == 2:
      a = argv[0]
      b = argv[1]
      return (self._seed / 2147483647) * (b - a) + a

min = 0
max = 2147483647

seed = 1238473661
# seed = time.time()

rnd = prng(seed)

def random():
  global rnd
  return math.floor(rnd.next(min, max))

def size():
  return len(alphabet)

def next_position(alphabet, char):
  j = random()
  position = alphabet.index(char)
  return (position + 1 + j) % size()

def previous_position(alphabet, char):
  j = random()
  position = alphabet.index(char)
  return size() - 1 - ((size() - position + j) % size())

def hex2binb(string):
  result = []
  while len(string) >= 8:
    result.append(int(string[:8], 16))
    string = string[8:]
  #return [i ^ 0xFFFFFFFF for i in result]
  return result

def shuffle(array, seed):
  rng = prng(seed)
  for i in reversed(range(len(array))):
    j = math.floor(rng.next(i))
    array[i], array[j] = array[j], array[i]

def shuffle_binb(alphabet, str):
  if isinstance(str, bytes):
    array = str
  else:
    array = hex2binb(str)
  shuffle(alphabet, array[0])
  shuffle(alphabet, array[1])
  shuffle(alphabet, array[2])
  shuffle(alphabet, array[3])
  shuffle(alphabet, array[4])
  shuffle(alphabet, array[5])
  shuffle(alphabet, array[6])
  shuffle(alphabet, array[7])
  shuffle(alphabet, array[8])
  shuffle(alphabet, array[9])
  shuffle(alphabet, array[10])
  shuffle(alphabet, array[11])
  shuffle(alphabet, array[12])
  shuffle(alphabet, array[13])
  shuffle(alphabet, array[14])
  shuffle(alphabet, array[15])

def cipher_function(cipher):
  def function(random, shift, alphabet, array, sha_alphabet, sha_plaintext):
    global rnd
    shuffle_binb(alphabet, sha_alphabet)
    shuffle_binb(alphabet, sha_plaintext)
    rnd = prng(random)
    i = 0
    while i < shift:
      array = list(map(cipher(alphabet), array))
      i = i + 1
    return list(array)
  return function

def shift_encrypt(alphabet):
  def enc(char):
    if char == '' or (not char in alphabet): raise Exception("undefined char '" + char + "'")
    position = alphabet.index(char)
    newPosition = next_position(alphabet, char)
    while newPosition == position:
      newPosition = next_position(alphabet, char)
    return alphabet[newPosition]
  return enc

def shift_decrypt(alphabet):
  def enc(char):
    if char == '' or (not char in alphabet): raise Exception("undefined char '" + char + "'")
    position = alphabet.index(char)
    newPosition = previous_position(alphabet, char)
    while newPosition == position:
      newPosition = previous_position(alphabet, char)
    return alphabet[newPosition]
  return enc

def encrypt_cipher(IV, shift, alphabet, plaintext, sha_alphabet, sha_plaintext):
  return cipher_function(shift_encrypt)(IV, shift, alphabet, plaintext, sha_alphabet, sha_plaintext)

def decrypt_cipher(IV, shift, alphabet, plaintext, sha_alphabet, sha_plaintext):
  return cipher_function(shift_decrypt)(IV, shift, alphabet, plaintext, sha_alphabet, sha_plaintext)

random_alphabet = [*alphabet]

import random as PRNG
#shuffle(random_alphabet, math.floor(rng * max))

alphabet = "".join(random_alphabet)


#alphabet = [chr(i) for i in range(0,0x10ffff)]
#PRNG.shuffle(alphabet)

encoded = encrypt_cipher(IV, shift, [*alphabet], [*plaintext], sha_alphabet, sha_plaintext)
print(encoded)

decoded = decrypt_cipher(IV, shift, [*alphabet], [*encoded], sha_alphabet, sha_plaintext)
print(decoded)
