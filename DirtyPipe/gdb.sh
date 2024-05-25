gdb \
    -ex "add-auto-load-safe-path /home/lvyzh/kernel/" \
    -ex "file /home/lvyzh/kernel/vmlinux" \
    -ex "target remote localhost:1234" \
    -ex "source page.py" \
    -ex "dprintf *(0xffffffff81208fdf), \"alloc pipe info  0x%llx\n\", \$rax" \
    -ex "c"
