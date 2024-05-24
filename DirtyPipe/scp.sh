gcc exp.c -o exp -static
scp -P 10021 -i ~/image/bullseye.id_rsa ./exp ./target_file root@localhost: