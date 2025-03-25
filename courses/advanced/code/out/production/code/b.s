		.globl main
	main:
		pushq	%rbp
		movq	%rsp, %rbp
	L_5:
		leaq L_6(%rip), %rdi
		callq	exn_frame_push
	L_7:
		leaq L_8(%rip), %rdi
		callq	exn_frame_push
		call throw0
		jmp	*%rax
		callq	 exn_frame_pop
		jmp	L_9
	L_8:
		callq	 exn_frame_pop
		movq $4, %rdi
		callq print
		jmp	L_9
	L_9:
		callq	 exn_frame_pop
		// select the normal return
		movq	8(%rbp), %rax
		movq	%rax, 16(%rbp)
		movq	(%rbp), %rax
		movq	%rax, 8(%rbp)
		addq	$8, %rbp
		// restore context
		leave
		ret
	L_6:
		callq	 exn_frame_pop
		// select the exn return
		movq	(%rbp), %rax
		movq	%rax, 8(%rbp)
		addq	$8, %rbp
		// restore context
		leave
		ret
