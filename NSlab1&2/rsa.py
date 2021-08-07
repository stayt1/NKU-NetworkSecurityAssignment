import rabin
#扩展欧几里得
def ex_gcd(a, b):
	if b == 0:
		return 1, 0
	else:
		k = a // b
		remainder = a % b
		x1, y1 = ex_gcd(b, remainder)
		x, y = y1, x1 - k*y1
	return x, y

#快速幂
def fast_expmod(b, e, m):
	result = 1
	while e != 0:
		if (e&1) == 1:
			result = (result * b) % m
		e >>= 1
		b = (b*b) % m
	return result

#生成公钥和密钥
def make_key(p,q,e):
	n=p*q
	fin=(p-1)*(q-1)
	d=ex_gcd(e,fin)[0]
	while d<0:
		d=(d+fin)%fin
	return [[n,e],[n,d]]

def generateKeyPair():
	return make_key(p,q,e)

#加密
def encryption(key,data):
	n,e=key
	data=list(data)
	out=[]
	for i in data:
		out.append(fast_expmod(ord(i),e,n))
	return out

#解密
def decrypt(key,data):
	n,d=key
	data=data
	out=''
	for i in data:
		out+=(chr(fast_expmod(i,d,n)))
	return out

p=rabin.get_prime(1024)
q=rabin.get_prime(1024)
# print('p:',p)
# print('q:',q)
# p=33478071698956898786044169848212690817704794983713768568912431388982883793878002287614711652531743087737814467999489
# q=36746043666799590428244633799627952632279158164343087642676032283815739666511279233373417143396810270092798736308917
e = 65537




# public_key,private_key=make_key(p,q,e)
# #
# Plaintext='Hello World!'
# print('明文:',Plaintext)
# ciphertext = encryption(public_key,Plaintext)
# print('密文:',ciphertext)
# Plaintext2=decrypt(private_key,ciphertext)
# print('解密明文:',Plaintext2)
#
# exit(0)
