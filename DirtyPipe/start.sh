qemu-system-x86_64 \
	-m 2G \
	-smp 2 \
	-kernel /home/lvyzh/kernel/arch/x86/boot/bzImage \
	-append "console=ttyS0 root=/dev/sda earlyprintk=serial net.ifnames=0 nokaslr" \
	-drive file=/home/lvyzh/image/bullseye.img,format=raw \
	-net user,host=10.0.2.10,hostfwd=tcp:127.0.0.1:10021-:22 \
	-net nic,model=e1000 \
	-nographic \
	-snapshot \
	-s
