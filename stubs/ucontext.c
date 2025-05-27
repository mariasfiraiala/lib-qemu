#include <ucontext.h>

void makecontext(struct __ucontext *ucp, void (*func)(), int argc, ...)
{
    return;
}

int swapcontext(struct __ucontext *restrict oucp, const struct __ucontext *restrict ucp)
{
    return 0;
}

int getcontext(struct __ucontext *ucp)
{
    return 0;
}

int setcontext(const struct __ucontext *ucp)
{
    return 0;
}
                