cpu:
	gcc -fPIC -shared hello.c -o hello.so

gpu:
	nvcc --compiler-options -fPIC -shared gpu.cu -o gpu.so
	cp gpu.so /tmp/

