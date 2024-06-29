.data
	newline:.asciiz "\n"   # Define una cadena de nueva línea en la sección de datos

.text

iniz:
    li $s1,0          # Inicializa $s1 con 0 (primer valor de la serie)
    li $s2,1          # Inicializa $s2 con 1 (segundo valor de la serie)
    li $s0,20         # Establece el límite de la serie en 7
    li $s4,1          # Inicializa el contador de iteraciones con 1
    j main            # Salta a la etiqueta 'main' para comenzar la serie

main:
    beq $s0,$0, iniz  # Si $s0 es igual a 0, salta a 'iniz' (punto de inicio)
    ble $s4,$s0, sum  # Si $s4 es menor o igual a $s0, salta a 'sum' (realiza la suma)
    li $v0,10         # Establece $v0 a 10 (código de syscall para salir)
    syscall           # Llama al sistema para terminar el programa

sum:
    move $a0,$s1      # Mueve el valor de $s1 a $a0 para imprimir
    add $a3,$s1,$s2   # Suma $s1 y $s2, almacena el resultado en $a3
    move $s1,$s2      # Mueve el valor de $s2 a $s1
    move $s2,$a3      # Mueve el valor de $a3 a $s2 (siguiente número en la serie)
    li $v0,1          # Establece $v0 a 1 (código de syscall para imprimir entero)
    syscall           # Llama al sistema para imprimir el valor en $a0
    la $a0,newline    # Carga la dirección de la nueva línea en $a0
    li $v0,4          # Establece $v0 a 4 (código de syscall para imprimir cadena)
    syscall           # Llama al sistema para imprimir la nueva línea
    addiu $s4,$s4,1   # Incrementa el contador $s4 en 1
    jal main          # Salta y enlaza a 'main' para la siguiente iteración