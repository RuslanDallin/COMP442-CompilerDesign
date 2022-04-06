% start of main
entry 
addi r14, r0, topaddr 



lw r1, None(r14)		% loading x
addi r14, r14, -4		% incrementing stack frame and starting printing
sw -8(r14),r1 
addi r1,r0, buf 
sw -12(r14),r1 
jl r15, intstr 
sw -8(r14),r13 
jl r15, putstr 
subi r14, r14, -4		% decremeting stack frame and starting printing


hlt 
buf res 20
