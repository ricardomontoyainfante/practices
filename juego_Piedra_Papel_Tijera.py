import random

count_user=0
count_machine=0
opc_user=""
opciones=("piedra", "papel", "tijera")
rounds=0

while(count_user<2 and count_machine<2):
    rounds+=1
    print("*"*15, "ROUND ", rounds, "*"*15)
    print("Marcador => | Machine:", count_machine, " | User: ", count_user)
    if not (opc_user in opciones):
        opc_user=input("Ingresa su opción: Piedra | Papel | Tijera => ").lower()

        if not (opc_user in opciones):
            rounds-=1
            continue

    opc_machine=random.choice(opciones)
    print("*"*10)
    print("Opción de Usuario: ", opc_user)
    print("Opción de Machine: ", opc_machine)

    if opc_machine==opc_user: 
        print("Empate!")
        opc_machine=opc_user=""
        continue

    elif opc_machine=="piedra":
        if opc_user=="papel":
            print("*"*15, " User Gana! ","*"*15)
            oopc_machine=opc_user=""
            count_user+=1
            continue
        else:
            print("*"*15,"Machine Gana!","*"*15)
            opc_machine=opc_user=""
            count_machine+=1
            continue
            
    elif opc_machine=="papel":
        if opc_user=="tijera":
            print("*"*15, " User Gana! ","*"*15)
            opc_machine=opc_user=""
            count_user+=1
            continue
        else:
            print("*"*15,"Machine Gana!","*"*15)
            opc_machine=opc_user=""
            count_machine+=1
            continue

    elif opc_machine=="tijera":
        if opc_user=="piedra":
            print("*"*15, " User Gana! ","*"*15)
            opc_machine=opc_user=""
            count_user+=1
            continue
        else:
            print("*"*15,"Machine Gana!","*"*15)
            opc_machine=opc_user=""
            count_machine+=1
            continue

print("*"*15," Fin del juego ", "*"*15)
print("Marcador => | Machine:", count_machine, " | User: ", count_user, " | Rounds: ", rounds)
print("*"*51)
count_user=count_machine=rounds=0
