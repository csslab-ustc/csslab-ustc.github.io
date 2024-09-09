#include<stdio.h>
#include<stdlib.h>
#include<pthread.h>
typedef int DataType;
typedef struct Stack
{
	DataType *_array;
	int _count;//空间能容纳的总元素
	int _size;//当前元素个数
}Stack;
typedef struct Args{
	Stack st;
	int x;
}Args;
void stackInit(Stack *st)//栈的初始化
{
	int n = 10000;
	st->_array = (DataType *)malloc(sizeof(DataType)*n);
	st->_count = n;
	st->_size = 0;
}
void print(Stack *st)//打印栈的元素，从底向上打印
{
	int count = st->_size;
	st->_size = 0;
	for (st->_size=0; st->_size < count; st->_size++)
	{
		printf("%d ", st->_array[st->_size]);
	}
	st->_size = count;
	printf("\n");
}
void* stackInsert(void* parameters)//入栈，尾插
{
	struct Stack* st = (struct Stack*)parameters;
	int x = 1;
	if (st->_size == st->_count)
	{
		st->_array = (DataType *)realloc(st->_array, sizeof(DataType) * 2 * st->_count);
		st->_count = 2 * st->_count;
	}
	st->_array[st->_size] = x;
	st->_size++;
	//print(st);
}
void stackDel(Stack *st)//出栈,每出栈一次栈顶元素就少一个
{
	if (st->_size > 0)
	{
		st->_size--;
		print(st);
	}
	else
	{
		printf("出栈错误，栈里已经没有元素了!!!\n");
	}
}
void stackTop(Stack *st)
{
	if (st->_size > 0)
	{
		printf("%d", st->_array[st->_size-1]);
		printf("\n");
	}
	else
	{
		printf("查找失败，栈里没有元素!!!\n");
	}
}
void stackSize(Stack *st)
{
	printf("%d", st->_size);
	printf("\n");
}
void stackEmpty(Stack *st)
{
	if (st->_size == 0)
	{
		printf("此时栈为空!!!\n");
	}
	else
	{
		printf("此时栈不为空!!!\n");
	}
}
void stackDestory(Stack *st)
{
	if (st->_array)
	{
		free(st->_array);
		st->_size = st->_count = 0;
		printf("栈已被销毁!!!\n");
	}
}
int main()
{
	Stack st;
	stackInit(&st);
	int count = 0;
	pthread_t tid[10000];
	pthread_t tid2;
	for(count = 0; count <10000; count++){
		pthread_create (&tid[count], NULL, stackInsert, &st);
		
	}
	for(count = 0; count <10000; count++){
		pthread_join(tid[count], NULL);
	}
	stackSize(&st);
	return 0;
}

