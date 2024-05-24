#define _GNU_SOURCE
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

void debug()
{
    puts("pause");
    getchar();
    return;
}

int main()
{
    int fd = open("./target_file", O_RDONLY);
    if (fd == -1)
    {
        perror("open");
        return 1;
    }
    printf("open success\n");

    debug();
    close(fd);
    return 0;
}