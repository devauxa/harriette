#include <sys/types.h>
#include <signal.h>
#include <stdlib.h>

int main(int ac, char **av) {
  setuid(1000);
  if (av[1][0] == '1') {
    kill(atoi(av[2]), 10);
  } else {
    kill(atoi(av[2]), 12);
  }
}
