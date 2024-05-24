gdb \
    -ex "add-auto-load-safe-path /home/lvyzh/kernel/" \
    -ex "file /home/lvyzh/kernel/vmlinux" \
    -ex "target remote localhost:1234" \
    -ex "b do_sys_openat2" \
    -ex "c"