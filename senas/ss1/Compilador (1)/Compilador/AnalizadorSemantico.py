from Nodo import nodo
from TablaHash import TablaHash
class AnalizadorSemantico:
    def __init__(self):
        self.archivo_errores = open("ErroresSemanticos.txt", "w")
        self.tabla=TablaHash()
        #self.archivo = open(".//IDE//Tokens.txt", "r")
        #self.tablaHash = open("Hash.txt", "w")
        print("ENTRO AL ARCHIVO")
        self.archivo_codigo = open("CodigoSemantica.txt", "w")
        self.location=0

    def asignType(self, arbol):
        if(arbol != None):
            if(arbol.tipoNodo == "DECLARACION"):
                arbol.hijos[0].tipoDec = arbol.tipoDec
            elif(arbol.tipoNodo == "EXPRESION"):
                if(arbol.tipoExp == "IDENTIFICADOR"):
                    arbol.hermanos.tipoExp = arbol.tipoExp

    #Inserta los datos a la tabla
    def insertTab(self,arbol):
        if(arbol.tipoNodo=="SENTENCIA"):
            if(arbol.tipoSen==":="):
                ID = self.tabla.hashTable[self.tabla.hashKey(arbol.nomIdExp)] # Se busca a la variable que se le quiere asignar
                if (ID != None): # Si el id que se busca es None significa que no esta declarada por lo cual no se agrega a la tabla
                    if(self.tabla.search(arbol.nomIdExp)==-1): #Si no se encuentra en la tabla lo crea
                        #insert(self,type,name,value,noLine,loc):
                        self.tabla.insert(arbol.tipoDec,arbol.nomIdExp,arbol.valCteExp,arbol.linea,self.location)
                        self.location = self.location + 1
                        #self.typeError(arbol,"VARIABLE NO DECLARADA")
                    else: #Se encuentra en la tabla y se ignora la locacion y solo se agrega la linea
                        self.tabla.insert(arbol.tipoDec, arbol.nomIdExp, arbol.valCteExp, arbol.linea, 0)
        elif(arbol.tipoNodo=="EXPRESION"):
            if(arbol.tipoExp=="IDENTIFICADOR"):
                if (self.tabla.search(arbol.nomIdExp) == -1):  # Si no se encuentra en la tabla lo crea
                    # insert(self,type,name,value,noLine,loc):
                    self.tabla.insert(arbol.tipoDec, arbol.nomIdExp, arbol.valCteExp, arbol.linea, self.location)
                    self.location = self.location + 1
                else:  # Se encuentra en la tabla y se ignora la locacion y solo se agrega la linea
                    self.tabla.insert(arbol.tipoDec, arbol.nomIdExp, arbol.valCteExp, arbol.linea, 0)

    #ERROR
    def typeError(self,arbol,msg):
        self.archivo_errores.write("ERROR EN LA LINEA: "+str(arbol.linea)+" -> "+msg+'\n')
        #arbol.valCteExp = "ERROR"
        arbol.error = "ERROR"

    #Pasando tipo
    def pasandoTipo(self, arbol):
        if(arbol != None):
            if(arbol.nomIdExp == "main"):
                self.pasandoTipo(arbol.hijos[0])
            elif(arbol.tipoNodo == "DECLARACION"): #Si es declaracion se pasa el tipo a la primer variable de la lista de variables
                arbol.hijos[0].tipoDec = arbol.tipoDec #El padre pasa el tipo al primer hijo de la lista de variables en la primer declaracion
                self.pasandoTipo(arbol.hijos[0]) #Se pasara el tipo a la lista de variables
                if(arbol.hermanos != None): #Si hay mas declaraciones se repite lo anterior
                    self.pasandoTipo(arbol.hermanos)
            elif(arbol.tipoNodo == "EXPRESION"):
                band = self.tabla.search(arbol.nomIdExp) #Se busca  que la variable no este en la tabla Hash
                if(band == -1):
                    self.insertTab(arbol) #Si no esta, entoncess se agrega
                else: #Como ya encontro la variable en alguna declaracion anterior, ya no se puede declarar nuevamente
                    #arbol.valCteExp = "ERROR"
                    arbol.error = "ERROR"
                    self.typeError(arbol,"VARIABLE " +arbol.nomIdExp+ " YA EXISTENTE") #Se Marca error
                if(arbol.hermanos != None):
                    arbol.hermanos.tipoDec = arbol.tipoDec #La primer variable pasara el tipo a las variables hermanas
                    self.pasandoTipo(arbol.hermanos)

    #Pasando Valor
    def pasandoValor(self,arbol):
        if(arbol != None):
            if(arbol.nomIdExp == "main"): #Si se encuentra en la raiz entonces se pasa al hijo[1] que son las sentencias
                self.pasandoValor(arbol.hijos[1])
            elif(arbol.tipoNodo == "SENTENCIA"):
                for i in range(len(arbol.hijos)):
                    if(self.pasandoValor(arbol.hijos[i]) != None):
                        self.pasandoValor(arbol.hijos[i])
# ******************ASIGNACION*************************************************************************************************************************************
                if(arbol.tipoSen == ":="): #Verificando que no sea un operador, si alguno es operador se tiene que bajar mas en el arbol
                    #self.pasandoValor(arbol.hijos[0])
                    pos = self.tabla.search(arbol.nomIdExp)  # Se busca  que la variable este en la tabla Hash para obtener su tipo actual
                    if (pos == -1):
                        #arbol.valCteExp = "ERROR"
                        # error es una bandera para saber si el valor es error ya no se podran realizar operaciones
                        # pero en la tabla hash se almacenara el ultimo valor que tuvo en el campo valCteExp y se mostrara este valor
                        arbol.error = "ERROR"
                        arbol.tipoDec = "ERROR"
                        self.typeError(arbol, "VARIABLE " + arbol.nomIdExp + " NO ENCONTRADA")  # Si no esta, entoncess se marca error
                    else:  # Como si se encontró la variable, se obtiene el tipo de la variable
                        arbol.tipoDec = self.tabla.hashTable[self.tabla.hashKey(arbol.nomIdExp)].type
                        if(arbol.tipoDec == str.lower(arbol.hijos[0].tipoDec)):
                            arbol.valCteExp = arbol.hijos[0].valCteExp #Se asigna el valor resultante
                            arbol.error = arbol.hijos[0].valCteExp  # Se asigna el valor resultante a la bandera de error
                            arbol.tipoDec = arbol.hijos[0].tipoDec #Se asigna el valor resultante
                        elif(arbol.tipoDec == "real" and str.lower(arbol.hijos[0].tipoDec) == "int"):
                            arbol.valCteExp = float(arbol.hijos[0].valCteExp) #Si el resultado es entero y la variable es real, se castea el resultado
                            arbol.error = float(arbol.hijos[0].valCteExp)  # Si el resultado es entero y la variable es real, se castea el resultado
                        #elif (arbol.tipoDec == "int" and str.lower(arbol.hijos[0].tipoDec) == "real"):
                            #arbol.valCteExp = int(float(arbol.hijos[0].valCteExp))  # Si el resultado es entero y la variable es real, se castea el resultado
                            # arbol.error = int(float(arbol.hijos[0].valCteExp))  # Si el resultado es entero y la variable es real, se castea el resultado
                        else:
                            #arbol.valCteExp = "ERROR"
                            arbol.error = "ERROR"
                            arbol.tipoDec = "ERROR"
                            self.typeError(arbol,"NO COINCIDEN TIPOS")
#*******************SENTENCIA IF**********************************************************************************************************************************
                elif(arbol.tipoSen == "if"):
                    if(arbol.hijos[0].tipoDec != "boolean"): #Si el resultado en la condicion no es un valor booleano, entonces se marca un error
                        arbol.hijos[0].valCteExp = "ERROR"
                        arbol.hijos[0].error = "ERROR"
                        arbol.hijos[0].tipoDec = "ERROR"
                        self.typeError(arbol.hijos[0], "CONDICION INVALIDA IF")  # Si no esta, entoncess se marca error
# *******************SENTENCIA WHILE**********************************************************************************************************************************
                elif (arbol.tipoSen == "while"):
                    if (arbol.hijos[0].tipoDec != "boolean"):  # Si el resultado en la condicion no es un valor booleano, entonces se marca un error
                        arbol.hijos[0].valCteExp = "ERROR"
                        arbol.hijos[0].error = "ERROR"
                        arbol.hijos[0].tipoDec = "ERROR"
                        self.typeError(arbol.hijos[0], "CONDICION INVALIDA WHILE")  # Si no esta, entoncess se marca error
# *******************SENTENCIA REPEAT**********************************************************************************************************************************
                elif (arbol.tipoSen == "repeat"):
                    if (arbol.hijos[1].tipoDec != "boolean"):  # Si el resultado en la condicion no es un valor booleano, entonces se marca un error
                        arbol.hijos[1].valCteExp = "ERROR"
                        arbol.hijos[1].error = "ERROR"
                        arbol.hijos[1].tipoDec = "ERROR"
                        self.typeError(arbol.hijos[1], "CONDICION INVALIDA REPEAT")  # Si no esta, entoncess se marca error
# *******************SENTENCIA COUT**********************************************************************************************************************************
                elif (arbol.tipoSen == "cout"):
                    if (arbol.hijos[0].error == "ERROR"):  # Si el valor es ERROR entonces es error
                        arbol.hijos[0].valCteExp = "ERROR"
                        arbol.hijos[0].error = "ERROR"
                        arbol.hijos[0].tipoDec = "ERROR"
                        self.typeError(arbol.hijos[0], "CONDICION INVALIDA")  # Si no esta, entoncess se marca error
                self.insertTab(arbol)
                if (arbol.hermanos != None):
                        self.pasandoValor(arbol.hermanos)
# ******************EXPRESION*************************************************************************************************************************************
            elif(arbol.tipoNodo == "EXPRESION"):
# ******************IDENTIFICADOR*************************************************************************************************************************************
                if(arbol.tipoExp == "IDENTIFICADOR"):
                    pos = self.tabla.search(arbol.nomIdExp)  # Se busca  que la variable este en la tabla Hash para obtener su valor actual
                    if (pos == -1): #Si no está, se marca el error
                        #arbol.valCteExp = "ERROR"
                        arbol.error = "ERROR"
                        arbol.tipoDec = "ERROR"
                        self.typeError(arbol, "VARIABLE "+arbol.nomIdExp+" NO ENCONTRADA")  # Si no esta, entoncess se marca error
                    else:  # Como si se encontró la variable, se obtiene el valor de la variable
                        reg = self.tabla.hashTable[self.tabla.hashKey(arbol.nomIdExp)]
                        if(reg.value != None):
                            arbol.tipoDec = self.tabla.hashTable[self.tabla.hashKey(arbol.nomIdExp)].type
                            arbol.valCteExp = self.tabla.hashTable[self.tabla.hashKey(arbol.nomIdExp)].value
                            arbol.error = self.tabla.hashTable[self.tabla.hashKey(arbol.nomIdExp)].value
                            self.insertTab(arbol)
                        else:
                            arbol.tipoDec = "ERROR"
                            arbol.error = "ERROR"
                            #arbol.valCteExp = "ERROR"
                            self.typeError(arbol, "VARIABLE "+arbol.nomIdExp+" SIN VALOR")  # Si no esta, entoncess se marca error
# ******************OPERADOR*************************************************************************************************************************************
                elif(arbol.tipoExp == "OPERADOR"):#Verificando que ninguno de los hijos sea un operador, si alguno es operador se tiene que bajar mas en el arbol
                    if (arbol.hijos[0].tipoExp == "OPERADOR" or arbol.hijos[0].tipoExp == "IDENTIFICADOR"):
                        self.pasandoValor(arbol.hijos[0])
                    if (arbol.hijos[1].tipoExp == "OPERADOR" or arbol.hijos[1].tipoExp == "IDENTIFICADOR"):
                        self.pasandoValor(arbol.hijos[1])
                    # Ya que ninguno sea operador, se verifica si los hijos son identificadores o constantes y se realiza la operacion
# ******************SUMA*************************************************************************************************************************************
                    if(arbol.OpExp == '+'):
                        # Si alguno de los operandos es un identificador, se busca en la tabla y se obtiene su valor
                        aux1 = None
                        aux2 = None
                        res = None
                        if (arbol.hijos[0].error != "ERROR" and arbol.hijos[1].error != "ERROR"): #Si ninguno de los dos valores es error, se realiza la operacion
                            aux1 = arbol.hijos[0].valCteExp
                            aux2 = arbol.hijos[1].valCteExp
                            res = eval(str(aux1) + '+' + str(aux2))  # Evalua para obtener el resultado de la operacion
                            arbol.valCteExp = res
                            arbol.error = res
                        else: #Si uno de los valores fue error, entonces no se puede realizar la operacion
                            #arbol.valCteExp = "ERROR"
                            arbol.error = "ERROR"
                            arbol.tipoDec = "ERROR"
                            self.typeError(arbol,"NO SE PUEDE REALIZAR LA OPERACION POR UN ERROR EN UN VALOR")
                            # Para definir el tipo del resultado
                        if (res != None and arbol.error != "ERROR"):
                            if (type(res) == float):
                                arbol.tipoDec = "real"
                            elif (type(res) == int):
                                arbol.tipoDec = "int"
                            elif (type(res) == bool):
                                arbol.tipoDec = "boolean"
                            else:
                                #arbol.valCteExp = "ERROR"
                                arbol.error = "ERROR"
                                arbol.tipoDec = "ERROR"
                                self.typeError(arbol, "TIPO DE DATO NO EXISTENTE")
# ******************RESTA*************************************************************************************************************************************
                    elif(arbol.OpExp == '-'):
                        # Si alguno de los operandos es un identificador, se busca en la tabla y se obtiene su valor
                        aux1 = None
                        aux2 = None
                        res = None
                        if (arbol.hijos[0].error != "ERROR" and arbol.hijos[1].error != "ERROR"):  # Si ninguno de los dos valores es error, se realiza la operacion
                            aux1 = arbol.hijos[0].valCteExp
                            aux2 = arbol.hijos[1].valCteExp
                            res = eval(str(aux1) + '-' + str(aux2))  # Evalua para obtener el resultado de la operacion
                            arbol.valCteExp = res
                            arbol.error = res
                        else:  # Si uno de los valores fue error, entonces no se puede realizar la operacion
                            arbol.tipoDec = "ERROR"
                            #arbol.valCteExp = "ERROR"
                            arbol.error = "ERROR"
                            self.typeError(arbol, "NO SE PUEDE REALIZAR LA OPERACION POR UN ERROR EN UN VALOR")
                            # Para definir el tipo del resultado
                        if (res != None and arbol.error != "ERROR"):
                            if (type(res) == float):
                                arbol.tipoDec = "real"
                            elif (type(res) == int):
                                arbol.tipoDec = "int"
                            elif (type(res) == bool):
                                arbol.tipoDec = "boolean"
                            else:
                                #arbol.valCteExp = "ERROR"
                                arbol.error = "ERROR"
                                arbol.tipoDec = "ERROR"
                                self.typeError(arbol, "TIPO DE DATO NO EXISTENTE")
# ******************MULTIPLICACION*************************************************************************************************************************************
                    elif (arbol.OpExp == '*'):
                     #Si alguno de los operandos es un identificador, se busca en la tabla y se obtiene su valor
                        aux1 = None
                        aux2 = None
                        res = None
                        if (arbol.hijos[0].error != "ERROR" and arbol.hijos[1].error != "ERROR"):  # Si ninguno de los dos valores es error, se realiza la operacion
                            aux1 = arbol.hijos[0].valCteExp
                            aux2 = arbol.hijos[1].valCteExp
                            res = eval(str(aux1) + '*' + str(aux2))  # Evalua para obtener el resultado de la operacion
                            arbol.valCteExp = res
                            arbol.error = res
                        else:  # Si uno de los valores fue error, entonces no se puede realizar la operacion
                            #arbol.valCteExp = "ERROR"
                            arbol.error = "ERROR"
                            arbol.tipoDec = "ERROR"
                            self.typeError(arbol, "NO SE PUEDE REALIZAR LA OPERACION POR UN ERROR EN UN VALOR")
                            # Para definir el tipo del resultado
                        if (res != None and arbol.error != "ERROR"):
                            if (type(res) == float):
                                arbol.tipoDec = "real"
                            elif (type(res) == int):
                                arbol.tipoDec = "int"
                            elif (type(res) == bool):
                                arbol.tipoDec = "boolean"
                            else:
                                #arbol.valCteExp = "ERROR"
                                arbol.error = "ERROR"
                                arbol.tipoDec = "ERROR"
                                self.typeError(arbol, "TIPO DE DATO NO EXISTENTE")
# ******************DIVISION*************************************************************************************************************************************
                    elif (arbol.OpExp == '/'):
                        # Si alguno de los operandos es un identificador, se busca en la tabla y se obtiene su valor
                        aux1 = None
                        aux2 = None
                        res = None
                        if (arbol.hijos[0].error != "ERROR" and arbol.hijos[1].error != "ERROR" and arbol.hijos[1].valCteExp != '0'):  # Si ninguno de los dos valores es error, se realiza la operacion
                            aux1 = arbol.hijos[0].valCteExp
                            aux2 = arbol.hijos[1].valCteExp
                            res = eval(str(aux1) + '/' + str(aux2))  # Evalua para obtener el resultado de la operacion
                            # Si ambos valores son enteros, se tiene que poner el resultado como entero ya que python lo regresa real
                            if (str.lower(arbol.hijos[0].tipoDec) == "int" and str.lower(arbol.hijos[1].tipoDec) == "int"):
                                arbol.valCteExp = int(float(res))
                                arbol.error = int(float(res))
                                #arbol.valCteExp = res
                            else:
                                arbol.valCteExp = res
                                arbol.error = res
                                # Para definir el tipo del resultado
                            if (res != None and arbol.error != "ERROR"):
                                if (type(res) == float):
                                    arbol.tipoDec = "real"
                                elif (type(res) == int):
                                    arbol.tipoDec = "int"
                                elif (type(res) == bool):
                                    arbol.tipoDec = "boolean"
                                else:
                                    #arbol.valCteExp = "ERROR"
                                    arbol.error = "ERROR"
                                    arbol.tipoDec = "ERROR"
                                    self.typeError(arbol, "TIPO DE DATO NO EXISTENTE")
                            else:  # Si uno de los valores fue error, entonces no se puede realizar la operacion
                                #arbol.valCteExp = "ERROR"
                                arbol.error = "ERROR"
                                arbol.tipoDec = "ERROR"
                                self.typeError(arbol, "NO SE PUEDE REALIZAR LA OPERACION POR UN ERROR EN UN VALOR")
                        else:  # Si uno de los valores fue error, entonces no se puede realizar la operacion
                            #arbol.valCteExp = "ERROR"
                            arbol.error = "ERROR"
                            arbol.tipoDec = "ERROR"
                            self.typeError(arbol, "NO SE PUEDE REALIZAR LA OPERACION POR UN ERROR EN UN VALOR")
# ******************DIFERENTE DE*************************************************************************************************************************************
                    elif (arbol.OpExp == '!='):
                        # Si alguno de los operandos es un identificador, se busca en la tabla y se obtiene su valor
                        aux1 = None
                        aux2 = None
                        res = None
                        if (arbol.hijos[0].error != "ERROR" and arbol.hijos[1].error != "ERROR"):  # Si ninguno de los dos valores es error, se realiza la operacion
                            aux1 = arbol.hijos[0].valCteExp
                            aux2 = arbol.hijos[1].valCteExp
                            res = eval(str(aux1) + '!=' + str(aux2))  # Evalua para obtener el resultado de la operacion (True o False)
                            arbol.valCteExp = res
                            arbol.error = res
                        else:  # Si uno de los valores fue error, entonces no se puede realizar la operacion
                            #arbol.valCteExp = "ERROR"
                            arbol.error = "ERROR"
                            arbol.tipoDec = "ERROR"
                            self.typeError(arbol, "NO SE PUEDE REALIZAR LA OPERACION POR UN ERROR EN UN VALOR")
                            # Para definir el tipo del resultado
                        if (res != None and arbol.error != "ERROR"):
                            if (type(res) == float):
                                arbol.tipoDec = "real"
                            elif (type(res) == int):
                                arbol.tipoDec = "int"
                            elif (type(res) == bool):
                                arbol.tipoDec = "boolean"
                            else:
                                #arbol.valCteExp = "ERROR"
                                arbol.error = "ERROR"
                                arbol.tipoDec = "ERROR"
                                self.typeError(arbol, "TIPO DE DATO NO EXISTENTE")
# ******************IGUAL QUE*************************************************************************************************************************************
                    elif (arbol.OpExp == '=='):
                        # Si alguno de los operandos es un identificador, se busca en la tabla y se obtiene su valor
                        aux1 = None
                        aux2 = None
                        res = None
                        if (arbol.hijos[0].error != "ERROR" and arbol.hijos[1].error != "ERROR"):  # Si ninguno de los dos valores es error, se realiza la operacion
                            aux1 = arbol.hijos[0].valCteExp
                            aux2 = arbol.hijos[1].valCteExp
                            res = eval(str(aux1) + '==' + str(aux2))  # Evalua para obtener el resultado de la operacion (True o False)
                            arbol.valCteExp = res
                            arbol.error = res
                        else:  # Si uno de los valores fue error, entonces no se puede realizar la operacion
                            #arbol.valCteExp = "ERROR"
                            arbol.error = "ERROR"
                            arbol.tipoDec = "ERROR"
                            self.typeError(arbol, "NO SE PUEDE REALIZAR LA OPERACION POR UN ERROR EN UN VALOR")
                            # Para definir el tipo del resultado
                        if (res != None and arbol.error != "ERROR"):
                            if (type(res) == float):
                                arbol.tipoDec = "real"
                            elif (type(res) == int):
                                arbol.tipoDec = "int"
                            elif (type(res) == bool):
                                arbol.tipoDec = "boolean"
                            else:
                                #arbol.valCteExp = "ERROR"
                                arbol.error = "ERROR"
                                arbol.tipoDec = "ERROR"
                                self.typeError(arbol, "TIPO DE DATO NO EXISTENTE")
# ******************MAYOR O IGUAL QUE*************************************************************************************************************************************
                    elif (arbol.OpExp >= '!='):
                        # Si alguno de los operandos es un identificador, se busca en la tabla y se obtiene su valor
                        aux1 = None
                        aux2 = None
                        res = None
                        if (arbol.hijos[0].error != "ERROR" and arbol.hijos[1].error != "ERROR"):  # Si ninguno de los dos valores es error, se realiza la operacion
                            aux1 = arbol.hijos[0].valCteExp
                            aux2 = arbol.hijos[1].valCteExp
                            res = eval(str(aux1) + '>=' + str(aux2))  # Evalua para obtener el resultado de la operacion (True o False)
                            arbol.valCteExp = res
                            arbol.error = res
                        else:  # Si uno de los valores fue error, entonces no se puede realizar la operacion
                            #arbol.valCteExp = "ERROR"
                            arbol.error = "ERROR"
                            arbol.tipoDec = "ERROR"
                            self.typeError(arbol, "NO SE PUEDE REALIZAR LA OPERACION POR UN ERROR EN UN VALOR")
                            # Para definir el tipo del resultado
                        if (res != None and arbol.error != "ERROR"):
                            if (type(res) == float):
                                arbol.tipoDec = "real"
                            elif (type(res) == int):
                                arbol.tipoDec = "int"
                            elif (type(res) == bool):
                                arbol.tipoDec = "boolean"
                            else:
                                #arbol.valCteExp = "ERROR"
                                arbol.error = "ERROR"
                                arbol.tipoDec = "ERROR"
                                self.typeError(arbol, "TIPO DE DATO NO EXISTENTE")
# ******************MAYOR DE*************************************************************************************************************************************
                    elif (arbol.OpExp == '>'):
                        # Si alguno de los operandos es un identificador, se busca en la tabla y se obtiene su valor
                        aux1 = None
                        aux2 = None
                        res = None
                        if (arbol.hijos[0].error != "ERROR" and arbol.hijos[1].error != "ERROR"):  # Si ninguno de los dos valores es error, se realiza la operacion
                            aux1 = arbol.hijos[0].valCteExp
                            aux2 = arbol.hijos[1].valCteExp
                            res = eval(str(aux1) + '>' + str(aux2))  # Evalua para obtener el resultado de la operacion (True o False)
                            arbol.valCteExp = res
                            arbol.error = res
                        else:  # Si uno de los valores fue error, entonces no se puede realizar la operacion
                            #arbol.valCteExp = "ERROR"
                            arbol.error = "ERROR"
                            arbol.tipoDec = "ERROR"
                            self.typeError(arbol, "NO SE PUEDE REALIZAR LA OPERACION POR UN ERROR EN UN VALOR")
                            # Para definir el tipo del resultado
                        if (res != None and arbol.error != "ERROR"):
                            if (type(res) == float):
                                arbol.tipoDec = "real"
                            elif (type(res) == int):
                                arbol.tipoDec = "int"
                            elif (type(res) == bool):
                                arbol.tipoDec = "boolean"
                            else:
                                #arbol.valCteExp = "ERROR"
                                arbol.error = "ERROR"
                                arbol.tipoDec = "ERROR"
                                self.typeError(arbol, "TIPO DE DATO NO EXISTENTE")
# ******************MENOR DE*************************************************************************************************************************************
                    elif (arbol.OpExp == '<'):
                        # Si alguno de los operandos es un identificador, se busca en la tabla y se obtiene su valor
                        aux1 = None
                        aux2 = None
                        res = None
                        if (arbol.hijos[0].error != "ERROR" and arbol.hijos[1].error != "ERROR"):  # Si ninguno de los dos valores es error, se realiza la operacion
                            aux1 = arbol.hijos[0].valCteExp
                            aux2 = arbol.hijos[1].valCteExp
                            res = eval(str(aux1) + '<' + str(aux2))  # Evalua para obtener el resultado de la operacion (True o False)
                            arbol.valCteExp = res
                            arbol.error = res
                        else:  # Si uno de los valores fue error, entonces no se puede realizar la operacion
                            #arbol.valCteExp = "ERROR"
                            arbol.error = "ERROR"
                            arbol.tipoDec = "ERROR"
                            self.typeError(arbol, "NO SE PUEDE REALIZAR LA OPERACION POR UN ERROR EN UN VALOR")
                            # Para definir el tipo del resultado
                        if (res != None and arbol.error != "ERROR"):
                            if (type(res) == float):
                                arbol.tipoDec = "real"
                            elif (type(res) == int):
                                arbol.tipoDec = "int"
                            elif (type(res) == bool):
                                arbol.tipoDec = "boolean"
                            else:
                                #arbol.valCteExp = "ERROR"
                                arbol.error = "ERROR"
                                arbol.tipoDec = "ERROR"
                                self.typeError(arbol, "TIPO DE DATO NO EXISTENTE")
# ******************MENOR O IGUAL QUE*************************************************************************************************************************************
                    elif (arbol.OpExp == '<='):
                        # Si alguno de los operandos es un identificador, se busca en la tabla y se obtiene su valor
                        aux1 = None
                        aux2 = None
                        res = None
                        if (arbol.hijos[0].error != "ERROR" and arbol.hijos[1].error != "ERROR"):  # Si ninguno de los dos valores es error, se realiza la operacion
                            aux1 = arbol.hijos[0].valCteExp
                            aux2 = arbol.hijos[1].valCteExp
                            res = eval(str(aux1) + '<=' + str(aux2))  # Evalua para obtener el resultado de la operacion (True o False)
                            arbol.valCteExp = res
                            arbol.error = res
                        else:  # Si uno de los valores fue error, entonces no se puede realizar la operacion
                            arbol.tipoDec = "ERROR"
                            #arbol.valCteExp = "ERROR"
                            arbol.error = "ERROR"
                            self.typeError(arbol, "NO SE PUEDE REALIZAR LA OPERACION POR UN ERROR EN UN VALOR")
                            # Para definir el tipo del resultado
                        if (res != None and arbol.error != "ERROR"):
                            if (type(res) == float):
                                arbol.tipoDec = "real"
                            elif (type(res) == int):
                                arbol.tipoDec = "int"
                            elif (type(res) == bool):
                                arbol.tipoDec = "boolean"
                            else:
                                arbol.tipoDec = "ERROR"
                                #arbol.valCteExp = "ERROR"
                                arbol.error = "ERROR"
                                self.typeError(arbol, "TIPO DE DATO NO EXISTENTE")
# ******************DIFERENTE DE*************************************************************************************************************************************
                    elif (arbol.OpExp == '!='):
                        # Si alguno de los operandos es un identificador, se busca en la tabla y se obtiene su valor
                        aux1 = None
                        aux2 = None
                        res = None
                        if (arbol.hijos[0].error != "ERROR" and arbol.hijos[1].error != "ERROR"):  # Si ninguno de los dos valores es error, se realiza la operacion
                            aux1 = arbol.hijos[0].valCteExp
                            aux2 = arbol.hijos[1].valCteExp
                            res = eval(str(aux1) + '!=' + str(aux2))  # Evalua para obtener el resultado de la operacion (True o False)
                            arbol.valCteExp = res
                            arbol.error = res
                        else:  # Si uno de los valores fue error, entonces no se puede realizar la operacion
                            arbol.tipoDec = "ERROR"
                            #arbol.valCteExp = "ERROR"
                            arbol.error = "ERROR"
                            self.typeError(arbol, "NO SE PUEDE REALIZAR LA OPERACION POR UN ERROR EN UN VALOR")
                            # Para definir el tipo del resultado
                        if (res != None and arbol.error != "ERROR"):
                            if (type(res) == float):
                                arbol.tipoDec = "real"
                            elif (type(res) == int):
                                arbol.tipoDec = "int"
                            elif (type(res) == bool):
                                arbol.tipoDec = "boolean"
                            else:
                                arbol.tipoDec = "ERROR"
                                #arbol.valCteExp = "ERROR"
                                arbol.error = "ERROR"
                                self.typeError(arbol, "TIPO DE DATO NO EXISTENTE")

#IMPRIMIR ARBOL
    def imprime_arbol_Sem(self, arbol, tabulaciones):
        tabulaciones = tabulaciones + 1
        while (arbol != None):
            self.imprime_espacios(tabulaciones)
            if (arbol.nomIdExp == "main"):
                self.archivo_codigo.write("PROGRAMA\n")
            elif (arbol.tipoNodo == "SENTENCIA"):
                if (arbol.tipoSen == "if"):
                    #self.archivo_codigo.write("If Tipo:"+arbol.hijos[0].tipoDec+" Valor:"+str(arbol.hijos[0].valCteExp)+"\n")
                    self.archivo_codigo.write("If Tipo:" + arbol.hijos[0].tipoDec + " Valor:" + str(arbol.hijos[0].error) + "\n")
                elif (arbol.tipoSen == "repeat"):
                    #self.archivo_codigo.write("Repeat Tipo:"+arbol.hijos[1].tipoDec+" Valor:"+str(arbol.hijos[1].valCteExp)+"\n")
                    self.archivo_codigo.write("If Tipo:" + str(arbol.hijos[0].tipoDec) + " Valor:" + str(arbol.hijos[1].error) + "\n")
                elif (arbol.tipoSen == ":="):
                    #self.archivo_codigo.write("Asignacion a variable: " + str(arbol.nomIdExp) + " Tipo:"+arbol.tipoDec+" Valor:"+str(arbol.valCteExp)+"\n")
                    self.archivo_codigo.write("Asignacion a variable: " + str(arbol.nomIdExp) + " Tipo:" + arbol.tipoDec + " Valor:" + str(arbol.error) + "\n")
                elif (arbol.tipoSen == "cin"):
                    self.archivo_codigo.write("Lectura variable: " + str(arbol.nomIdExp) + "\n")
                elif (arbol.tipoSen == "cout"):
                    #self.archivo_codigo.write("Escritura Tipo:"+arbol.hijos[0].tipoDec+" Valor:"+str(arbol.hijos[0].valCteExp)+"\n")
                    self.archivo_codigo.write("Escritura Tipo:" + arbol.hijos[0].tipoDec + " Valor:" + str(arbol.hijos[0].error) + "\n")
                elif (arbol.tipoSen == "bloque"):
                    self.archivo_codigo.write("Bloque: \n")
                elif (arbol.tipoSen == "break"):
                    self.archivo_codigo.write("Break; \n")
                elif (arbol.tipoSen == "while"):
                    #self.archivo_codigo.write("While Tipo:"+arbol.hijos[0].tipoDec+" Valor:"+str(arbol.hijos[0].valCteExp)+"\n")
                    self.archivo_codigo.write("While Tipo:" + arbol.hijos[0].tipoDec + " Valor:" + str(arbol.hijos[0].error) + "\n")
                else:
                    self.archivo_codigo.write("Nodo de tipo SENTENCIA, DESCONOCIDO\n")
            elif (arbol.tipoNodo == "EXPRESION"):
                if (arbol.tipoExp == "OPERADOR"):
                    #self.archivo_codigo.write("Operador: " + str(arbol.OpExp) + " Tipo:"+arbol.tipoDec+" Valor:"+str(arbol.valCteExp)+"\n")
                    self.archivo_codigo.write("Operador: " + str(arbol.OpExp) + " Tipo:" + arbol.tipoDec + " Valor:" + str(arbol.error) + "\n")
                elif (arbol.tipoExp == "REAL" or arbol.tipoExp == "INT"):
                    self.archivo_codigo.write("Constante: " + str(arbol.valCteExp) + " Tipo:"+arbol.tipoDec+"\n")
                    #self.archivo_codigo.write("Constante: " + str(arbol.error) + "Tipo:" + arbol.tipoDec + "\n")
                elif (arbol.tipoExp == "REAL" or arbol.tipoExp == "INT"):
                    self.archivo_codigo.write("Constante: " + str(arbol.valCteExp) + " Tipo:"+arbol.tipoDec+"\n")
                    #self.archivo_codigo.write("Constante: " + str(arbol.error) + "Tipo:" + arbol.tipoDec + "\n")
                elif (arbol.tipoExp == "IDENTIFICADOR"):
                    #self.archivo_codigo.write("Id: " + str(arbol.nomIdExp) + " Tipo:"+arbol.tipoDec+" Valor:"+str(arbol.valCteExp)+"\n")
                    self.archivo_codigo.write("Id: " + str(arbol.nomIdExp) + " Tipo:" + arbol.tipoDec + " Valor:" + str(arbol.error) + "\n")
                else:
                    self.archivo_codigo.write("Nodo de tipo EXPRESION, DESCONOCIDO\n")
            elif (arbol.tipoNodo == "DECLARACION"):
                if (arbol.tipoDec == "int"):
                    self.archivo_codigo.write("Variable int: " + "\n")
                elif (arbol.tipoDec == "real"):
                    self.archivo_codigo.write("Variable real: " + "\n")
                elif (arbol.tipoDec == "boolean"):
                    self.archivo_codigo.write("Variable boolean: " + "\n")
                else:
                    self.archivo_codigo.write("Nodo de tipo EXPRESION, DESCONOCIDO\n")
            else:
                self.archivo_codigo.write("Tipo de NODO, DESCONOCIDO\n")

            for i in range(3):
                self.imprime_arbol_Sem(arbol.hijos[i],tabulaciones)
            arbol = arbol.hermanos
        tabulaciones = tabulaciones -1

    # IMPRIME ESPACIOS EN ARBOL
    def imprime_espacios(self, tabulaciones):
        for i in range(tabulaciones):
            self.archivo_codigo.write(" ")

    def cierra_archivos(self):
        self.archivo_codigo.close()
        self.archivo_errores.close()