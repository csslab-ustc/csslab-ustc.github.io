		.data
	f_name:
		.string "f"
		.text
		.globl f
	f:
		pushq	%rbp
		movq	%rsp, %rbp
	L_10:
		leaq	L_11(%rip), %rdi
		callq	exn_frame_push
		movq	$9, %rdi
		callq	print
		call throw0
		jmp	*%rax
		callq	exn_frame_pop
		// restore context
		leave
		ret
	L_11:
		callq	exn_frame_pop
		leaq	f_name(%rip), %rdi
		callq	cleanup
		callq	exn_frame_pop
		movq	%rax, 8(%rbp)
		// restore context
		leave
		ret
		.data
	main0_name:
		.string "main0"
		.text
		.globl main0
	main0:
		pushq	%rbp
		movq	%rsp, %rbp
	L_12:
		leaq	L_13(%rip), %rdi
		callq	exn_frame_push
	L_14:
		leaq	L_15(%rip), %rdi
		callq	exn_frame_push
		callq	f
		callq	exn_frame_pop
		jmp	L_16
	L_15:
		callq	exn_frame_pop
		movq	$4, %rdi
		callq	print
		jmp	L_16
	L_16:
		callq	exn_frame_pop
		// restore context
		leave
		ret
	L_13:
		callq	exn_frame_pop
		leaq	main0_name(%rip), %rdi
		callq	cleanup
		callq	exn_frame_pop
		movq	%rax, 8(%rbp)
		// restore context
		leave
		ret
		.globl main
	main:
		pushq	%rbp
		movq	%rsp, %rbp
		leaq	topHandler(%rip), %rdi
		callq	exn_frame_push
		callq	main0
		callq	exn_frame_pop
		leave
		ret
		

	.section .note.GNU-stack
