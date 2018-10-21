/* -- first.s */
.data
.balign 4
a: .skip 64



.text
.balign 4
.global main
.func main
main:
    outerLoop:
        cmp r0, #6
        bgt end1
        add r1, r0, #0          /*set inner loop variable*/

        ldr r2, [=a, +r0, LSL #2]
        innerLoop:
            cmp r1,#7
            bgt end2

            ldr r3, [=a, +r1, LSL #2] 
            /* if statement here, r2 is swap pos*/
            if_eval:
                cmp r2, r3
            blt end_if
            then:
                add r2, r3, #0
                mov r4, [=a, +r1, LSL #2]
                b end_if
            end_if:

            add r1, r1, #1
            b innerLoop
            end2:
        ldr r5, [=a, +r0, LSL #2]   /*lower swap value*/
        ldr r6, [r4]                /*upper swap value*/
        str r5, [r4] 
        str r6, [=a, +r0, LSL #2] 
        
        add r1, r1, #1
        b outerLoop
        end1:

    bx lr
