/* -- sort.s */
.data
.balign 4
a:
    .skip 64
    .word 1,5,8,0,13,12,8,7,6,9,3,4,2,2,1,6

min:
	.word 0

min_addr:
	.word 0

count1:
	.word 0

count2:
	.word 0

.text
.balign 4
.global main
.func main
main:
    outerLoop:
	ldr r1, =count1
	ldr r0, [r1]
        cmp r0, #6
        bgt end1
        add r0, r0, #1          /*set inner loop variable*/
	str r0, [r1]

	ldr r1, =a
        ldr r2, [r1, +r0, LSL #2]
        innerLoop:
	    ldr r1, =count2
	    ldr r0, [r1]
            cmp r0, #2
            bgt end2
	    add r0, r0, #1
	    str r0, [r1]

	    ldr r1, =a
            ldr r3, [r1, +r0, LSL #2]
            /* if statement here, r2 is swap pos*/
            if_eval:
                cmp r2, r3
            bge end_if
            then:
		ldr r1, =min_addr
		str r0, [r1]
		ldr r0, =min
		str r3, [r0]
                b end_if
            end_if:
            b innerLoop
            end2:/*
	ldr r0, =a
	ldr r1, =min_addr
	ldr r1, [r1]
        ldr r2, [r0, +r1, LSL #2]   /*upper swap value*/
/*	ldr r2, [r2]
        ldr r3, [r0]                /*lower swap value*/
/*        str r2, [r0]
        str r3, [r0, +r1, LSL #2]

        add r1, r1, #1*/
        b outerLoop
        end1:

    bx lr
addr_a: .word a
addr_min: .word min
addr_min_addr: .word min_addr
