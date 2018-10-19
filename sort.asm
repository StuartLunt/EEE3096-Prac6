/* -- first.s */
.data
.balign 4
a: .skip 24



.text
.balign 4
.global main
.func main
main:
    outerLoop:
        cmp r0, #6
        bgt end
        add r1, r0, #0          /*set inner loop variable*/

        innerLoop:
            cmp r1,#7
            bgt end
            /* if statement here, r2 is swap pos*/
            

            add r1, r1, #1
            b loop
        
        ldr r3, [=a, +r0, LSL #2]   /*lower swap value*/
        ldr r4, [=a, +r2, LSL #2]   /*upper swap value*/
        str r3, [=a, +r2, LSL #2] 
        str r4, [=a, +r0, LSL #2] 
        
        add r1, r1, #1
        b loop

    bx lr
