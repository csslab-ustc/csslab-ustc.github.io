		.globl f
	f:
		pushq	%rbp
		movq	%rsp, %rbp
	L_10:
		leaq L_11(%rip), %rdi
		callq	exn_frame_push
		movq $9, %rdi
		callq print
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
	L_11:
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
	L_12:
		leaq L_13(%rip), %rdi
		callq	exn_frame_push
	L_14:
		leaq L_15(%rip), %rdi
		callq	exn_frame_push
		pushq	L_18(%rip)
		pushq	L_17(%rip)
		jmp	f
	L_17:
		jmp	L_19
	L_18:
		// select the exn return
		movq	(%rbp), %rax
		movq	%rax, 8(%rbp)
		addq	$8, %rbp
		// restore context
		leave
		ret
	L_19:
		callq	 exn_frame_pop
		jmp	L_16
	L_15:
		callq	 exn_frame_pop
		movq $4, %rdi
		callq print
		jmp	L_16
	L_16:
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
	L_13:
		callq	 exn_frame_pop
		// select the exn return
		movq	(%rbp), %rax
		movq	%rax, 8(%rbp)
		addq	$8, %rbp
		// restore context
		leave
		ret
