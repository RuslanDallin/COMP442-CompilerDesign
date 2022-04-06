% start of main
entry 
addi r14, r0, topaddr 



addi r1, r0, 2		% t1 = 2 * 3
addi r2, r0, 3
mul r3, r1, r2
sw -16(r14), r3


addi r1, r0, 1		% t2 = 1 + t1
lw r2, -16(r14)
add r3, r1, r2
sw -20(r14), r3


lw r1, -20(r14)		% assigning y = t2
sw -8(r14), r1


addi r14, r14, -48		% reading subroutine: incrementing stack frame and starting
addi r1,r0, buf 
sw -8(r14),r1 
jl r15, getstr 
jl r15, strint
subi r14, r14, -48		% reading subroutine: decremeting stack frame and starting printing
sw -4(r14), r13		% storing input into x


lw r2, -8(r14)		% t3 = y + 10
addi r3, r0, 10
add r4, r2, r3
sw -24(r14), r4


lw r2, -4(r14)		% t4 = x > t3
lw r3, -24(r14)
cgt r4, r2, r3
sw -28(r14), r4


lw r1, -28(r14)		% loading t4
bz r1 , else1


lw r1, -4(r14)		% t5 = x + 10
addi r2, r0, 10
add r3, r1, r2
sw -32(r14), r3


lw r1, -32(r14)		% loading t5
addi r14, r14, -48		% writing subroutine: incrementing stack frame and starting
sw -8(r14),r1 
addi r1,r0, buf 
sw -12(r14),r1 
jl r15, intstr 
sw -8(r14),r13 
jl r15, putstr 
subi r14, r14, -48		% writing subroutine: decremeting stack frame and starting


j endIf1
else1 nop
lw r1, -4(r14)		% t6 = x + 1
addi r2, r0, 1
add r3, r1, r2
sw -36(r14), r3


lw r1, -36(r14)		% loading t6
addi r14, r14, -48		% writing subroutine: incrementing stack frame and starting
sw -8(r14),r1 
addi r1,r0, buf 
sw -12(r14),r1 
jl r15, intstr 
sw -8(r14),r13 
jl r15, putstr 
subi r14, r14, -48		% writing subroutine: decremeting stack frame and starting


endIf1 nop
addi r1, r0, 10		% assigning z = 10
sw -12(r14), r1


goWhile1 nop
lw r1, -12(r14)		% t7 = z >= 2
addi r2, r0, 2
cge r3, r1, r2
sw -40(r14), r3


lw r1, -40(r14)		% loading t7
bz r1 , endWhile1


lw r1, -12(r14)		% t8 = z - 2
addi r2, r0, 2
sub r3, r1, r2
sw -44(r14), r3


lw r1, -44(r14)		% assigning z = t8
sw -12(r14), r1


lw r1, -12(r14)		% loading z
addi r14, r14, -48		% writing subroutine: incrementing stack frame and starting
sw -8(r14),r1 
addi r1,r0, buf 
sw -12(r14),r1 
jl r15, intstr 
sw -8(r14),r13 
jl r15, putstr 
subi r14, r14, -48		% writing subroutine: decremeting stack frame and starting


j goWhile1
endWhile1 nop
hlt 
buf res 20
