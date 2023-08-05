import random   #Libreria utilizada para generar un numero aleatorio para el comprobante
import datetime #Libreria utilizada para usar la fecha y hora


def cargar_apuestas_quiniela():
    '''
    Esta funcion lee las apuestas en el archivo y almacena cada linea en la lista datos,
    el elemento 1 de datos corresponde al modo en que se hizo la apuesta (Quiniela o Quini 6 Tradicional),
    por lo que se utiliza este elemento para comprobar si la linea leida corresponde a una apuesta de 
    Quiniela o de Quini 6 Tradicional. En esta funcion solo interesan las apuestas de Quiniela, por lo que
    las apuestas de Quini 6 no se almacenaran el la lista 'apuestas_quiniela'.
    '''
    apuestas_quiniela = []
    with open("ProyectoFinal\\apuestas.txt", "r") as file:
        for linea in file:
            datos = linea.strip().split(";") #dividir cada linea de apuesta leida en base al elemento ';'
            if datos[1] == "Quiniela": #comprobar si la apuesta corresponde a Quiniela
                apostador = datos[3] #Si corresponde, almacenar el dni del apostador
                numero_apostado = int(datos[5]) #Tambien almacenar el numero apostado, convertido a entero
                apuestas_quiniela.append([apostador, numero_apostado]) #Agregar dni y apuesta de la linea leida en un elemento de la lista
    return apuestas_quiniela


def cargar_apuestas_quini_6():
    '''
    Similar a la funcion cargar_apuestas_quiniela() pero con la finalidad de comprobar si la linea leida
    es de una apuesta de Quini 6 Tradicional.
    '''
    apuestas_quini_6 = []
    numeros_apostados = []
    with open("ProyectoFinal\\apuestas.txt", "r") as file:
        for linea in file:
            datos = linea.strip().split(";") #dividir cada linea de apuesta leida en base al elemento ';'
            if datos[1] == "Quini 6 tradicional": #comprobar si la apuesta corresponde a Quini 6 Tradicional
                apostador = datos[3] #Si corresponde, almacenar el dni del apostador
                numeros_apostados = [int(numero) for numero in datos[5].split(",")] #Tambien almacenar el numero apostado, convertido a entero
                apuestas_quini_6.append([apostador, numeros_apostados]) #Agregar dni y apuesta de la linea leida en un elemento de la lista
    return apuestas_quini_6


def imprimir_comprobante(quiniela, apostador, cifras_apostadas, monto):
    '''
    Esta funcion se encarga de imprimir en pantalla el comprobante, se le debe
    pasar como parametro el nombre de la quiniela, el dni del apostador, la/s
    cifras apostadas y el monto apostado. Teniendo estos datos los mostrara en
    pantalla
    '''
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #obtener la fecha y hora actual, y luego lo formatearla como una cadena en el formato "AAAA-MM-DD HH:MM:SS"
    numero_comprobante = random.randint(10000, 99999)                  #genera un numero entero random de 5 cifras
    print("***************************************************")
    print(f"******** Comprobante - {quiniela} ********")
    print("***************************************************")
    print(f"Fecha y hora de la apuesta: {fecha_hora}")
    print(f"Número de comprobante: {numero_comprobante}")
    print(f"DNI del apostador: {apostador}")
    print(f"Monto: {monto}")
    if isinstance(cifras_apostadas, list):  #Esto se hace debido a que cifras apostadas puede ser una lista de 6 numeros (quini 6) o un solo numero (quiniela)
        print(f"Cifras apostadas: {', '.join(str(cifra) for cifra in cifras_apostadas)}")  #compresion de lista para convertir cada cifra en cifras apostadas en dato de tipo string. Luego mediante ", ".join se combina cada cifra para formar una cadena con los 6 numeros que contiene la lista cifras_apostadas 
    else:
        print(f"Cifra apostada: {cifras_apostadas}") #Si no es una lista 'isinstance(cifras_apostadas, list) devolvera false y se ingresara al else, por lo que cifras_apostadas tendra solo un numero que es el de la quiniela
    print("****************************************************\n")


def guardar_apuesta_en_archivo(quiniela, apostador, cifras_apostadas, monto):
    '''
    Esta funcion se utiliza para registrar o guardar cada apuesta en un archivo que esta
    dentro de la carpeta del proyecto final, se lo abre al archivo en el modo append para
    que no se sobreescriba todo el archivo y la apuesta se registre al final del archivo.
    '''
    with open("ProyectoFinal\\apuestas.txt", "a") as archivo:
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        numero_comprobante = random.randint(10000, 99999)
        apuesta = f"{fecha_hora};{quiniela};{numero_comprobante};{apostador};{monto};"
        if isinstance(cifras_apostadas, list): # esta funcion retorna true si cifras_apostadas es una instancia de lista, es decir, si es una lista. Sino, retorna false
            apuesta += ",".join(str(cifra) for cifra in cifras_apostadas) #se recorre cada cifra en la lista cifras_apostadas y se las convierte en string, seguido a esto se las escribe en la misma linea en el archivo. Cada cifra esta separada por una coma
        else:
            apuesta += str(cifras_apostadas) # si no es una lista, es el numero de la quiniela, por lo que se escribe el numero convertido a string, en la misma linea
        apuesta += "\n" # Añadir un salto de línea para separar cada apuesta en líneas diferentes
        archivo.write(apuesta)
      
        
def validar_dni(dni):
    '''
    Funcion que se encarga de verificar si el dni pasado como parametro
    es solo numericos y tambien se encarga de comprobar si su longitud
    es de 7 u 8 cifras (debido a que en Argentina lo habitual es que 
    una persona cuente con dni de 7 u 8 cifras)
    '''
    # Verificar que el DNI tenga 7 u 8 caracteres
    if len(dni) not in [7, 8]:
        return False

    # Verificar que el DNI esté compuesto solo de dígitos numéricos
    if not dni.isdigit():
        return False

    return True


def quiniela():
    '''
    Esta funcion se utiliza cuando el usuario escoge apostar a la Quiniela, primero solicita
    la cantidad de cifras que va a tener el numero a apostar y hasta que el usuario no coloque
    un numero correcto, el programa no dejara de pedirle. Seguido a esto se le solicita el dni
    del apostador y luego el numero a apostar, el cual debe coincidir con la cantidad de cifras
    que el apostador eligio.
    '''
    print("Has seleccionado: Quiniela")
    cifras_apostadas = [] #lista vacia, la cual va a almacenar el numero apostado
    while True:
        num_cifras = input("Selecciona el número de cifras a apostar (2, 3 o 4): ")
        if num_cifras in ('2', '3', '4'): #Si el numero de num_cifras esta dentro de esta tupla, sale del while y continua con el codigo
            break
        else:
            print("Opción inválida. Por favor, selecciona 2, 3 o 4.")
            
    while True:
        dni_apostador = input("Ingresa tu DNI: ")
        if validar_dni(dni_apostador):  #si retorna true, sale del while, dando como indicio de que el numero ingresado cumple con un dni argentino (7 u 8 digitos y solo numerico)
            break
        else:
            print("El DNI no es válido. Por favor, intenta nuevamente.")
    
    while True:
        cifra = input(f"Ingrese {num_cifras} cifras para apostar: ")
        if str(len(cifra)) == num_cifras: #comprobar si el largo de cifra es igual al numero de cifras que el usario eligio
            break #salir del while y continuar con las siguientes lineas de codigo
        else:
            print("El numero ingresado no coincide con las cifras elegidas. Por favor ingrese el numero correcto.")
    
    while True: #while 1
        # Se utiliza manejo de excepciones debido a que si el usuario ingresa un dato que no es tipo numerico, se provoca un error, por lo que se imprimira en pantalla un mensaje en vez del error
        try:
            while True: #while 2
                monto = input("Ingrese el monto a apostar: ")
                if int(monto) == 0: # No se puede apostar 0 pesos
                    print(f"Debes apostar un monto superior a {monto} pesos")
                elif int(monto) < 0: # Tampoco se puede apostar numeros negativos
                    print("No se permite apostar numeros inferiores a 0")
                else:
                    break # Sale del while 2
            break #sale del while 1
        except ValueError:
            print("Debes ingresar solo numeros")
    imprimir_comprobante("Quiniela 'LOS POLLOS HERMANOS'", dni_apostador, cifra, monto)
    guardar_apuesta_en_archivo("Quiniela", dni_apostador, cifra, monto)


def generar_numeros_aleatorios(cantidad):
    '''
    Esta funcion solamente se encarga de generar numeros aleatorios entre 0 y 45(inclusive)
    por lo que se utiliza la funcion sample() que toma como parametro el rango de numeros
    y la cantidad. Esta funcion retorna una lista de 6 numeros aleatorios generados, en el 
    rango de 0 a 45.
    '''
    return random.sample(range(46), cantidad)


def quini_6_tradicional():
    '''
    Esta funcion se utiliza cuando el usuario quiere apostar al Quini 6 Tradicional,
    primero pide el dni del usuario, luego le pregunta si desea generar los numeros
    al azar o si los desea ingresar el mismo. Por ultimo le solicita el monto y llama
    a las funciones para imprimir el comprobante y para guardar la apuesta en el archivo
    '''
    print("Has seleccionado: Quini 6 tradicional")
    while True:
        dni_apostador = input("Ingresa tu DNI: ")
        if validar_dni(dni_apostador):  #si retorna true, sale del while, dando como indicio de que el numero ingresado cumple con un dni argentino (7 u 8 digitos y solo numerico)
            break
        else:
            print("El DNI no es válido. Por favor, intenta nuevamente.")
            
    while True:
        opcion = input("Deseas generar los números al azar? (Sí: S / No: N): ")
        if opcion.upper() == 'S': # se utiliza el metodo upper para comprobar solamente si es mayusculas, ya que el usuario puede ingresar en minusculas pero esto no dificultara nada
            cifras_apostadas = generar_numeros_aleatorios(6)  #llama a la funcion se le pasa 6 como parametro, el resultado se almacena en cifras apostadas (lista)
            break
        elif opcion.upper() == 'N':
            cifras_apostadas = [] #la declara vacia ya que se almacenaran los numeros ingresados por el usuario
            print("Ingresa 6 números entre 0 y 45 (inclusive) para apostar:")
            print("Presiona ENTER por cada numero ingresado")
            while len(cifras_apostadas) < 6: #ejecutara este while siempre que cifras apostadas sea menor a 6, ya que solo debe contener 6 numeros, partiendo del 0 al 5
                cifra = input()
                if cifra.isdigit() and 0 <= int(cifra) <= 45 and int(cifra) not in cifras_apostadas:
                    #primero se comprueba si cifra es digito mediante isdigit() cuyo resultado es true si lo es, 
                    #luego se verifica si cifra esta entre 0 y 45 convirtiendolo primero a entero. 
                    #Por ultimo se verifica que el valor de cifra no este dentro de la lista ya que no puede haber numeros repetidos
                    cifras_apostadas.append(int(cifra)) #agrega la cifra a la lista, convirtiendola a entero
                else:
                    print("Número inválido o repetido. Ingrese un número válido entre 0 y 45.")
            break
        else:
            print("Ingrese el caracter correcto (S/N)")
                
                
    while True: #while 1
        # Se utiliza manejo de excepciones debido a que si el usuario ingresa un dato que no es tipo numerico, se provoca un error, por lo que se imprimira en pantalla un mensaje en vez del error
        try:
            while True: #while 2
                monto = input("Ingrese el monto a apostar: ")
                if int(monto) == 0: # No se puede apostar 0 pesos
                    print(f"Debes apostar un monto superior a {monto} pesos")
                elif int(monto) < 0: # Tampoco se puede apostar numeros negativos
                    print("No se permite apostar numeros inferiores a 0")
                else:
                    break # Sale del while 2
            break #sale del while 1
        except ValueError:
            print("Debes ingresar solo numeros")
    imprimir_comprobante("Quini 6 tradicional", dni_apostador, cifras_apostadas, monto)
    guardar_apuesta_en_archivo("Quini 6 tradicional", dni_apostador, cifras_apostadas, monto)


def comprobar_apuesta_ganadora():
    '''
    Esta funcion se encarga de comprobar si la apuesta ingresada por el usuario, es decir, la apuesta
    ganadora, coincide con alguna de las apuestas que se encuentren en el archivo. Primero se le pregunta
    al usuario si desea buscar en las apuestas de Quiniela o de Quini 6 Tradicional. Una vez elegido el modo,
    el usuario ingresara el o los numeros correspondientes al modo elegido y se comprobara si la apuesta ganadora
    existe en el archivo y en base a eso se mostrara en pantalla si el usuario gano o no.
    '''
    print("Has seleccionado: Comprobar Apuesta")
    print("1. Quiniela")
    print("2. Quini 6 tradicional")
    while True:
        opcion = input("Selecciona una opción (1 o 2): ")

        if opcion == '1':
            while True:
                apuesta_str = input("Ingresa el número apostado para Quiniela: ")
                if apuesta_str.isdigit(): #si la apuesta ingresada es un dijito, lo pasa a entero. Si no es entero, se le pide al usuario que ingrese un numero valido
                    apuesta = int(apuesta_str)
                    break  # Si se ingresó un número válido, salimos del ciclo y continuamos con la validación
                print("Error: Debes ingresar un número válido. Intenta nuevamente.")

            apuestas_quiniela = cargar_apuestas_quiniela()  #Esta variable va almacenar el dni del usuario y la apuesta que dicho dni hizo, en formato de lista
            
            for apostador, numero_apostado in apuestas_quiniela: #Se utiliza un for para recorrer los elementos de la lista y almacenar el dni en apostador y la apuesta en numero_apostado
                if apuesta == numero_apostado:  #Si la apuesta ingresada por el usuario coincide con el numero_apostado en la iteracion, el dni apostador es ganador
                    print(f"¡Felicidades! El numero {numero_apostado} apostado para Quiniela coincide con la apuesta ganadora.")
                    print(f"DNI del ganador: {apostador}")
                    return   #Salir de la funcion y no buscar más coincidencias una vez que se ha encontrado una.
            print("Lo siento, la apuesta para Quiniela no coincide con ninguna apuesta ganadora.")
            break

        elif opcion == '2':
            '''
            Para determinar si una apuesta es ganadora, el orden de los numeros ingresados debe ser el mismo
            que el de los numeros guardados en el archivo. De lo contrario se tomara como apuesta no ganadora.
            '''
            while True:
                apuesta_str = input("Ingresa los 6 números apostados para Quini 6 separados por comas: ")
                
                try:
                    numeros_apostados = [int(numero) for numero in apuesta_str.split(",")]  #comprensión de lista que recorre cada elemento de la lista generada en el paso anterior y convierte cada elemento a un número entero utilizando int(numero)
                    if len(numeros_apostados) == 6 and len(set(numeros_apostados)) == 6:  #Verificar si se ingresaron 6 numeros y tambien si los mismos no estan repetidos
                        break  # Si se ingresaron 6 números, salimos del ciclo y continuamos con la validación. Esta verificacion se hace debido a que en Quini 6 Tradicional se apuestan 6 numeros, ni mas ni menos
                    else:
                        print("Error: Debes ingresar exactamente 6 números. Intenta nuevamente.")
                except ValueError:
                     print("Error: Ingresa solo NÚMEROS separados por comas. Intenta nuevamente.")
            
            apuestas_quini_6 = cargar_apuestas_quini_6()  #Cargar en apuestas_quini_6 la lista que contiene elementos con el dni del apostador y los 6 numeros que dicho apostador uso

            for apostador, numeros_apostados_guardados in apuestas_quini_6:
                if numeros_apostados == numeros_apostados_guardados:  #Verificar si los numeros apostados coinciden con los numeros apostados guardados
                    numeros_apostados_str = str(numeros_apostados).replace("[", "").replace("]", "")  # Convertir la lista en una cadena y eliminar los corchetes
                    print(f"¡Felicidades! Los números {numeros_apostados_str} apostados para Quini 6 coinciden con la apuesta ganadora.")
                    print(f"DNI del ganador: {apostador}")
                    return  #Salir de la funcion y no buscar más coincidencias una vez que se ha encontrado una.

            print("Lo siento, los números apostados para Quini 6 no coinciden con ninguna apuesta ganadora.")
            break

        else:
            print("Opción inválida. Por favor, selecciona una opción válida (1 o 2).")
            

def cargar_apuestas_desde_archivo():
    '''
    Funcion que se encarga de leer las apuestas en el archivo y en base a los ';'
    va separando los datos para almacenarlos en una lista y retornarlos
    '''
    apuestas = []
    try:
        with open("ProyectoFinal\\apuestas.txt", "r") as archivo:
            for linea in archivo:  #Leer cada linea en el archivo
                datos = linea.strip().split(";") #datos es una lista que contendra la linea en el archivo en cada iteracion y cada elemento de datos sera un dato relacionado a la apuesta leida en la linea, ya que se separa cada dato por los ';'
                quiniela = datos[1] #quiniela va a contener el modo (Quiniela o Quini 6 Tradicional). Es importante para cuando se llame a la funcion cargar_apuestas_quiniela() o cargar_apuestas_quini_6()
                dni_apostador = datos[3] #almacenar el dni del apostador
                monto = float(datos[4]) #almacenar el monto apostado en la linea leida
                cifras_apostadas = datos[5] # lista que contiene los numeros apostados. En caso de que datos[5] sea una lista (6 numeros para quini 6), la lista tendra 6 elementos, mientras que para Quiniela, solo tendra un elemento (no habra comas)
                apuestas.append([quiniela, dni_apostador, cifras_apostadas, monto])
    except FileNotFoundError:
        pass
    return apuestas


def calcular_recaudacion_diaria():
    '''
    Esta funcion se encarga de llamar a la funcion cargar_apuestas_desde_archivo(), la cual
    retorna una lista cuyos elementos contienen los datos de cada apuesta. Esta funcion solamente
    toma el monto de cada apuesta y los agrega a una lista llamada 'montos', luego recorre esta lista
    y cada monto convertido a su tipo entero se va sumando y almacenando en la variable recaudacion_diaria.
    Por ultimo se retorna la recaudacion diaria, para ser utilizada en arqueo_de_caja()
    '''
    apuestas = cargar_apuestas_desde_archivo()
    recaudacion_diaria = 0
    montos = []
    for apuesta in apuestas:
        montos.append(apuesta[3])  #Almacenar los montos en la lista
    for monto in montos:
        recaudacion_diaria += int(monto) #Sumar los montos
    return recaudacion_diaria


def arqueo_de_caja():
    '''
    Esta funcion se encarga de realizar el arqueo de caja, para ello se obtiene la recaudacion
    diaria y a la misma se le calcula la retencion del estado. Luego, se calcula la ganancia 
    neta siendo la diferencia entre las dos. Y por ultimo, se muestran los datos en pantalla
    '''
    recaudacion_diaria = calcular_recaudacion_diaria()
    retencion_estado = recaudacion_diaria * 0.47
    ganancia_neta = recaudacion_diaria - retencion_estado
    print("Has seleccionado: Arqueo de caja")
    print("Recaudación diaria en apuestas:", recaudacion_diaria)
    print("Retención del Estado (47%):", round(retencion_estado, 2)) #Redondear a 2 cifras decimales
    print("Ganancia neta para el quinielero:", round(ganancia_neta, 2)) #Redondear a 2 cifras decimales
    print("************************************************\n")


def salir_menu():
    '''
    Funcion que al ser llamada, mostrara un mensaje de despedida en pantalla
    '''
    print("Gracias por usar nuestro sistema de quiniela. ¡Hasta pronto!")


def mostrar_menu():
    print("************************************************")
    print("-------- Quiniela 'Los Pollos Hermanos' --------")
    print("************************************************")
    print("1. Quiniela")
    print("2. Quini 6 tradicional")
    print("3. Comprobar apuesta")
    print("4. Arqueo de caja")
    print("5. Salir")

while True:
    mostrar_menu()
    opcion = input("Selecciona una opción (1-5): ")

    if opcion == '1':
        quiniela()
    elif opcion == '2':
        quini_6_tradicional()
    elif opcion == '3':
        comprobar_apuesta_ganadora()
    elif opcion == '4':
        arqueo_de_caja()
    elif opcion == '5':
        salir_menu()
        break
    else:
        print("Opción inválida. Por favor, selecciona una opción válida (1-5).")
