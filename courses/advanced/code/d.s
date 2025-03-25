		.globl main0
	main0:
		pushq	%rbp
		movq	%rsp, %rbp
	L_20:
		leaq L_21(%rip), %rdi
		callq	exn_frame_push
		call throw0
		jmp	*%rax
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
	L_21:
		callq	 exn_frame_pop
		// select the exn return
		movq	(%rbp), %rax
		movq	%rax, 8(%rbp)
		addq	$8, %rbp
		// restore context
		leave
		ret
		.globl main
	main:
		pushq	%rbp
		movq	%rsp, %rbp
		leaq	topHandler(%rip), %rax
		pushq	%rax
		callq	main0
		leave
		ret
		

	.section .note.GNU-stack
