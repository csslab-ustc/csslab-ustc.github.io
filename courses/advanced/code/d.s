		.data
	main0_name:
		.string "main0"
		.text
		.globl main0
	main0:
		pushq	%rbp
		movq	%rsp, %rbp
	L_17:
		leaq	L_18(%rip), %rdi
		callq	exn_frame_push
		call throw0
		jmp	*%rax
		callq	exn_frame_pop
		// restore context
		leave
		ret
	L_18:
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
