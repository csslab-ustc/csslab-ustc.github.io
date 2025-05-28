// To compile and run:
//   $ g++ ssa.cpp; ./a.out

#include <cstdio>
#include <cstdlib>
#include <functional>

// the original function, in source code form
// figure 5.4(a)
int f_src(){
  int i = 1, j = 1, k = 0;
  while(k<100){
    if(j<20){
      j = i;
      k = k + 1;
    }else{
      j = k;
      k = k + 2;
    }
  }
  return j;
}

// the original function, in control-flow graph form
// figure 5.4(a)
int f_cfg(){
  int i, j, k;

L1:
  i = 1;
  j = 1;
  k = 0;
  goto L2;

L2:
  if(k<100) goto L3; else goto L4;

L3:
  if(j<20) goto L5; else goto L6;

L5:
  j = i;
  k = k + 1;
  goto L7;

L6:
  j = k;
  k = k + 2;
  goto L7;

L7:
  goto L2;

L4:
  return j;
}

// the SSA function
// figure 5.7(b)
// where the control-flow originates
static char *from;

static int phi(int l, char *l_label, int r, char *r_label){
  if(strcmp(from, l_label) == 0)
    return l;
  return r;
}

int f_ssa(){
  int i1, j1, k1,
  i2, j2, k2,
  i3, j3, k3,
  j4, k4,
  j5, k5;

L1:
  i1 = 1,
  j1 = 1,
  k1 = 0;
  from = "L1";
  goto L2;

L2:
  j2 = phi(j1, "L1", j5, "L7");
  k2 = phi(k1, "L1", k5, "L7");
  if(k2<100) goto L3; else goto L4;

L3:
  if(j2<20) goto L5; else goto L6;

L5:
  j3 = i1;
  k3 = k2 + 1;
  from = "L5";
  goto L7;

L6:
  j4 = k2;
  k4 = k2 + 2;
  from = "L6";
  goto L7;

L7:
  j5 = phi(j3, "L5", j4, "L6");
  k5 = phi(k3, "L5", k4, "L6");
  from = "L7";
  goto L2;

L4:
  return j2;
}

// the function, in functional programming form
// figure ???
void f_fun(void (*halt)(int)){

  std::function<void(void)> L1 = [&](){
    int i1 = 1;
    int j1 = 1;
    int k1 = 0;

    std::function<void(int, int)> L2 = [&](int j2, int k2) -> void {
      std::function<void(void)> L3 = [&](){
        std::function<void(int, int)> L7 = [&](int j5, int k5){
          L2(j5, k5);
        };
        std::function<void(void)> L5 = [&](){
          int j3 = i1;
          int k3 = k2 + 1;
          L7(j3, k3);
        };
        std::function<void(void)> L6 = [&](){
          int j4 = k2;
          int k4 = k2 + 2;
          L7(j4, k4);
        };
        if(j2<20) L5(); else L6();
      };
      std::function<void(void)> L4 = [&](){
        halt(j2);
      };
      if(k2<100) L3(); else L4();
    };
    L2(j1, k1);
  };
  L1();
}

int main(){
  printf("f_src()=%d\n", f_src());
  printf("f_cfg()=%d\n", f_cfg());
  printf("f_ssa()=%d\n", f_ssa());
  f_fun([](int x){printf("f_fun()=%d\n", x); exit(0);});

  return 0;
}

