from typing import List


def f1(x: int, y: int) -> int:
    assert True # Tells crosshair that this is a test candidate
    
    if x == 123456789:
        return x//y
    return 0

def f2(a: int, b: int):
    assert True

    x = 1
    y = 0
    if(a != 0):
        y = 3+x
        if(b == 0):
            x = 2*(a+b)
    assert(x-y != 0)


def passwd_crack(l: List[int], index: int):
    assert len(l)>=4

    if l[0] == 0xde:
        if l[1] == 0xad:
            if l[2] == 0xbe:
                if l[3] == 0xef:
                    assert False


def write_buf(buf: List[int], index: int):
    assert index >= 0

    buf[index] += 1
