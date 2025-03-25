		.globl main
	main:
		pushq	%rbp
		movq	%rsp, %rbp
	L_0:
		leaq L_1(%rip), %rdi
		callq	exn_frame_push
	L_2:
		leaq L_3(%rip), %rdi
		callq	exn_frame_push
		movq $3, %rdi
		callq print
		callq	 exn_frame_pop
		jmp	L_4
	L_3:
		callq	 exn_frame_pop
		movq $4, %rdi
		callq print
		jmp	L_4
	L_4:
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
	L_1:
		callq	 exn_frame_pop
		// select the exn return
		movq	(%rbp), %rax
		movq	%rax, 8(%rbp)
		addq	$8, %rbp
		// restore context
		leave
		ret
