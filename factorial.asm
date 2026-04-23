main:        
        #simulate .data section by simulating start of memory storing data
        #set start of mem
        addi $s0, $zero, 0 

        addi $t9, $zero, 10
        nop
        nop
        sw $t9, 0($s0) #int stored in memory at 0
        #answer will be in memory at 4 bytes from start
        
        and $t9, $t9, $zero #resets register $t9
        
        #get value to factorialize
        lw $t0, 0($s0)
        nop
        nop    
        beq $t0, $zero, base_case
        nop
        nop
        addi $t1, $zero, 1
        nop
        nop    
factorial_func:    #mult fac
        mul $t1, $t1, $t0
        addi $t0, $t0, -1
        nop
        nop

        beq $t0, $zero, finish_fac
        nop
        nop

        j factorial_func
        nop
        nop
        
base_case:     #handle 0 by setting result to 1
        addi $t1, $zero, 1
        nop
        nop
        
        
finish_fac:    #store result
        sw $t1, 4($s0) #store answer in memory
        
        #end program
        nop