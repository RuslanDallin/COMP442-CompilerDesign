% start of f
f sw -8(r14), r15


lw r1, -16(r14)		% t1 = p2 * p3
lw r2, -20(r14)
mul r3, r1, r2
sw -28(r14), r3


lw r1, -12(r14)		% t2 = p1 + t1
lw r2, -28(r14)
add r3, r1, r2
sw -32(r14), r3


lw r1, -32(r14)		% assigning retval = t2
sw -24(r14), r1


lw r1, -24(r14)		% return retval
sw 0(r14), r1
lw r15, -8(r14)		% jump to calling function 
jr r15 


% start of temp
temp sw -8(r14), r15


addi r1, r0, 4		% t1 = 4 * 2
addi r2, r0, 2
mul r3, r1, r2
sw -28(r14), r3


lw r1, -28(r14)		% assigning c = t1
sw -24(r14), r1


lw r1, -16(r14)		% t2 = p3 - c
lw r2, -24(r14)
sub r3, r1, r2
sw -32(r14), r3


lw r1, -32(r14)		% assigning tempa = t2
sw -20(r14), r1


lw r1, -20(r14)		% return tempa
sw 0(r14), r1
lw r15, -8(r14)		% jump to calling function 
jr r15 


% start of main
entry 
addi r14, r0, topaddr 



addi r1, r0, 1		% assigning a = 1
sw -4(r14), r1


addi r1, r0, 2		% assigning b = 2
sw -8(r14), r1


addi r1, r0, 3		% assigning c = 3
sw -12(r14), r1


lw r1, -4(r14)		% pass a into p1
sw -44(r14), r1
lw r1, -8(r14)		% pass b into p2
sw -48(r14), r1
lw r1, -12(r14)		% pass c into p3
sw -52(r14), r1


addi r14, r14, -32		% increment stack frame
jl r15, f
subi r14, r14, -32		% decrement stack frame
lw r1, -32(r14)		% t1 = f
sw -16(r14), r1


lw r1, -4(r14)		% pass a into p1
sw -44(r14), r1
lw r1, -12(r14)		% pass c into p3
sw -48(r14), r1


addi r14, r14, -32		% increment stack frame
jl r15, temp
subi r14, r14, -32		% decrement stack frame
lw r1, -32(r14)		% t2 = temp
sw -20(r14), r1


lw r1, -16(r14)		% t3 = t1 * t2
lw r2, -20(r14)
mul r3, r1, r2
sw -24(r14), r3


lw r1, -24(r14)		% assigning a = t3
sw -4(r14), r1


addi r1, r0, 4		% t4 = 4 * -7
addi r2, r0, -7
mul r3, r1, r2
sw -28(r14), r3


lw r1, -28(r14)		% loading t4
addi r14, r14, -32		% incrementing stack frame and starting printing
sw -8(r14),r1 
addi r1,r0, buf 
sw -12(r14),r1 
jl r15, intstr 
sw -8(r14),r13 
jl r15, putstr 
subi r14, r14, -32		% decremeting stack frame and starting printing


hlt 
buf res 20
