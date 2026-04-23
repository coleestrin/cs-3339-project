# EXAMPLE ASM FILE FOR TESTING

ADDI $t0, $zero, 5
NOP
NOP
NOP
ADDI $t1, $zero, 3
NOP
NOP
NOP
ADD  $t2, $t0, $t1
SUB  $t3, $t0, $t1
MUL  $t4, $t0, $t1
AND  $t5, $t0, $t1
OR   $t6, $t0, $t1
SLL  $t7, $t0, 1
SRL  $t8, $t0, 1
SW   $t2, 0($zero)
LW   $s0, 0($zero)
BEQ  $t0, $t0, skip
NOP
skip:
J    done
done:
NOP
