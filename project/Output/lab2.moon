% start of main
entry 
addi r14, r0, topaddr 



addi r1, r0, 65		% assigning x = 65
sw -4(r14), r1


lw r2, -4(r14)		% t1 = x <> 1
addi r3, r0, 1
cne r4, r2, r3
sw -8(r14), r4


lw r1, -8(r14)		% loading t1
bz r1 , else1


lw r3, -4(r14)		% t2 = x < 5
addi r4, r0, 5
clt r5, r3, r4
sw -12(r14), r5


lw r2, -12(r14)		% loading t2
bz r2 , else2


addi r3, r0, 1		% assigning x = 1
sw -4(r14), r3


j endIf2
else2 nop
addi r3, r0, 0		% assigning x = 0
sw -4(r14), r3


endIf2 nop
j endIf1
else1 nop
addi r2, r0, 66		% assigning x = 66
sw -4(r14), r2


endIf1 nop
lw r1, -4(r14)		% loading x
addi r14, r14, -16		% incrementing stack frame and starting printing
sw -8(r14),r1 
addi r1,r0, buf 
sw -12(r14),r1 
jl r15, intstr 
sw -8(r14),r13 
jl r15, putstr 
subi r14, r14, -16		% decremeting stack frame and starting printing


hlt 
buf res 20
