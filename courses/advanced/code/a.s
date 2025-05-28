		.data
	main0_name:
		.string "main0"
		.text
		.globl main0
	main0:
		pushq	%rbp
		movq	%rsp, %rbp
	L_0:
		leaq	L_1(%rip), %rdi
		callq	exn_frame_push
	L_2:
		leaq	L_3(%rip), %rdi
		callq	exn_frame_push
		movq	$3, %rdi
		callq	print
		callq	exn_frame_pop
		jmp	L_4
	L_3:
		callq	exn_frame_pop
		movq	$4, %rdi
		callq	print
		jmp	L_4
	L_4:
		callq	exn_frame_pop
		// restore context
		leave
		ret
	L_1:
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
