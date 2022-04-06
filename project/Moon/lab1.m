% start of main
entry 
addi r14, r0, topaddr 



addi r1, r0, 2		% assigning y = 2
sw -12(r14), r1


addi r1, r0, 5		% assigning x = 5
sw -8(r14), r1


addi r1, r0, 8		% assigning x = 8
sw -8(r14), r1


lw r1, -8(r14)		% loading x
addi r14, r14, -16		% writing subroutine: incrementing stack frame and starting
sw -8(r14),r1 
addi r1,r0, buf 
sw -12(r14),r1 
jl r15, intstr 
sw -8(r14),r13 
jl r15, putstr 
subi r14, r14, -16		% writing subroutine: decremeting stack frame and starting


lw r1, -8(r14)		% loading x
addi r14, r14, -16		% writing subroutine: incrementing stack frame and starting
sw -8(r14),r1 
addi r1,r0, buf 
sw -12(r14),r1 
jl r15, intstr 
sw -8(r14),r13 
jl r15, putstr 
subi r14, r14, -16		% writing subroutine: decremeting stack frame and starting


hlt 
buf res 20
