from Nodo import nodo
class AnalizadorSintaxis:
    def __init__(self):
        self.lineaToken = 0
        self.error = False
        self.token = None
        self.tipoToken = None
        self.archivo_errores = open("ErroresSintaxis.txt", "w")
#        self.archivo = open(".//IDE//Tokens.txt", "r")
        self.archivo = open("Tokens.txt", "r")
        print("ENTRO AL ARCHIVO")
        self.archivo_codigo = open("CodigoSintaxis.txt", "w")

    def nodoDeclara(self, tipoDec):
        t = nodo()
        t.tipoNodo = "DECLARACION"
        t.tipoDec = tipoDec
        t.linea = self.lineaToken
        return t

    def nodoExpresion(self, tipoExp):
        t = nodo()
        t.tipoNodo = "EXPRESION"
        t.tipoExp = tipoExp
        t.tipoDec = self.tipoToken
        t.linea = self.lineaToken
        return t

    def nodoSentencia(self, tipoSen):
        t = nodo()
        t.tipoNodo = "SENTENCIA"
        t.tipoSen = tipoSen
        t.linea = self.lineaToken
        return t

    #MENSAJES DE ERROR
    def syntaxError(self, mensaje):
        self.archivo_errores.write("ERROR EN LA LINEA: " + str(self.lineaToken) +" "+ mensaje + "\n")
        self.error = True

    #SIGUIENTE TOKEN
    def sigToken(self):
        linea = self.archivo.readline()
        datos = linea.split('\t')
        self.lineaToken = datos[2] #GUARDA LA LINEA EN QUE SE ENCONTRÓ EL TOKEN EN EL ARCHIVO ORIGINAL
        self.columnaToken = datos[3]  #GUARDA LA COLUMNA EN QUE SE ENCONTRÓ EL TOKEN EN EL ARCHIVO ORIGINAL
        self.tipoToken = datos[1]  #GUARDA EL TIPO DEL TOKEN
        return datos[0]  #REGRESA EL TOKEN

    #VERIFICAR QUE EL TOKEN ACTUAL SEA EL QUE SE ESPERA
    def match(self, esperado):
        if(self.token == esperado):  #ESTO NO TIENE SENTIDO PORQUE LA PRIMERA VEZ QUE MATCH ES LLAMADO TOKEN ES NULO ENTONCES QUE COMPARA?! O SI TIENE UN VALOR??
            self.token = self.sigToken()
        else:
            self.syntaxError("TOKEN NO ESPERADO -> " + self.token + " " + self.tipoToken)
            #imprimeToken(token,tipoToken)

    #PROGRAMA
    def programa(self):
        self.token = self.sigToken()  # REGRESA EL TOKEN
        t = nodo()
        t.nomIdExp= self.token
        self.match("main")
        self.match("{")
        if (t != None):
            t.hijos[0] = self.lista_declaraciones()
            t.hijos[1] = self.lista_sentencias()
        self.match("}")
        return t

    #LISTA DE DECLARACIONES
    def lista_declaraciones(self): #declaracion { declaracion }
        t = None
        while (self.token != "ENDFILE" and self.token != ";" and self.token != "}" and self.token != "until" and self.token != "if" and
                self.token != "while" and self.token != "do" and self.token != "repeat" and self.token != "then" and self.token != "else" and
                    self.token != "end" and self.token != "cin" and self.token != "cout" and self.tipoToken != "IDENTIFICADOR"):
            q = self.declaracion()
            if (q != None):
                if (t == None):
                    t = p = q
                else:
                    p.hermanos = q
                    p = q
        return t

    #DECLARACION
    def declaracion(self):
        t = None
        if (self.token == "int" or self.token == "real" or self.token == "boolean"):
            t = self.nodoDeclara(self.token)
            self.match(self.token)
            if(t != None):
                t.hijos[0] = self.lista_variables()
            self.match(";")
        else:
            self.syntaxError("TOKEN NO ESPERADO -> " + self.token + " " + self.tipoToken)
            self.token = self.sigToken()
        return t

    #LISTA DE VARIABLES
    def lista_variables(self):
        t = None
        if (self.tipoToken == "IDENTIFICADOR"):
            t = self.nodoExpresion(self.tipoToken)
            t.nomIdExp = self.token
            self.token = self.sigToken()
            p = t
            while(self.token == ","):
                self.match(",")
                q = self.nodoExpresion("IDENTIFICADOR")
                if (q != None):
                    if (t == None):
                        t = p = q
                    else:
                        if (self.tipoToken == "IDENTIFICADOR"):
                            q.nomIdExp = self.token
                            p.hermanos = q
                            p = q
                self.token = self.sigToken()
        else:
            self.syntaxError("TOKEN NO ESPERADO -> " + self.token + " " + self.tipoToken)
            self.token = self.sigToken()
        return t

    #LISTA DE SENTENCIAS
    def lista_sentencias(self):
        t = None
        while (self.token != "ENDFILE" and self.token != "else" and self.token != "{" and self.token != "until" and self.token != "then" and self.token != "}"):
            q = self.sentencia()
            if (q != None):
                if (t == None):
                    t = p = q
                else:
                    p.hermanos = q
                    p = q
        return t

    #SENTENCIA
    def sentencia(self):
        t = None
        if(self.token == "if"):
            t = self.seleccion()
        elif(self.token == "while"):
            t = self.iteracion()
        elif (self.token == "repeat"):
            t = self.repeticion()
        elif(self.tipoToken == "IDENTIFICADOR"):
            t = self.asignacion()
        elif(self.token == "cin"):
            t = self.sent_cin()
        elif(self.token == "cout"):
            t = self.sent_cout()
        elif(self.token == "{"):
            t = self.bloque()
        elif (self.token == "break"):
            t = self.senbreak()
        else:
            self.syntaxError("TOKEN NO ESPERADO -> " + self.token + " " + self.tipoToken)
            self.token = self.sigToken()
        return t

    #SELECCION
    def seleccion(self):
        t = self.nodoSentencia("if")
        self.match("if")
        self.match("(")
        if(t != None):
            t.hijos[0] = self.expresion()
        self.match(")")
        self.match("then")
        if (t != None):
            t.hijos[1]= self.bloque()
        if(self.token == "else"):
            self.match("else")
            if(t != None):
                t.hijos[2] = self.bloque()
        return t

    #ITERACION
    def iteracion(self):
        t = self.nodoSentencia("while")
        self.match("while")
        self.match("(")
        if(t != None):
            t.hijos[0] = self.expresion()
        self.match(")")
        if (t != None):
            t.hijos[1]= self.bloque()
        return t

    #REPETICION
    # def repeticion(self):
    #     t = self.nodoSentencia("repeat")
    #     self.match("repeat")
    #     if (t != None):
    #         t.hijos[0] = self.bloque()
    #     self.match("until")
    #     self.match("(")
    #     if (t != None):
    #         t.hijos[1] = self.expresion()
    #     self.match(")")
    #     self.match(";")
    #     return t

    #READ
    def sent_cin(self):
        aux = None
        t = self.nodoSentencia("cin")
        self.match("cin")
        if(t != None):
            if(self.tipoToken == "IDENTIFICADOR"):
                t.hijos[0] = self.expresion()
                aux = t
            else:
                self.syntaxError("TOKEN NO ESPERADO -> " + self.token + " " + self.tipoToken)
                self.token = self.sigToken()
        self.match(";")
        return aux

    #WRITE
    def sent_cout(self):
        t = self.nodoSentencia("cout")
        self.match("cout")
        if (t != None):
            t.hijos[0] = self.expresion()
        self.match(";")
        return t

    #BLOQUE
    def bloque(self):
        t = self.nodoSentencia("bloque")
        self.match("{")
        if (t != None):
            t.hijos[0] = self.lista_sentencias()
        self.match("}")
        return t

    #BREAK
    def senbreak(self):
        t = self.nodoSentencia("break")
        self.match("break")
        self.match(";")
        return t

    #ASIGNACION
    def asignacion(self):
        t = None
        if(self.tipoToken == "IDENTIFICADOR"):
            t = self.nodoSentencia(":=")
            t.nomIdExp = self.token
        self.token = self.sigToken()
        if(self.token == "++"):
            self.match("++")
            p = self.nodoExpresion("OPERADOR")
            if (p != None):
                p.OpExp = '+'
                x = self.nodoExpresion("IDENTIFICADOR")
                x.nomIdExp = t.nomIdExp
                p.hijos[0] = x
                y = self.nodoExpresion("INT")
                y.valCteExp = '1'
                y.tipoDec = "int"
                p.hijos[1] = y
                t.hijos[0] = p
        elif(self.token == "--"):
            self.match("--")
            p = self.nodoExpresion("OPERADOR")
            if (p != None):
                p.OpExp = '-'
                x = self.nodoExpresion("IDENTIFICADOR")
                x.nomIdExp = t.nomIdExp
                p.hijos[0] = x
                y = self.nodoExpresion("INT")
                y.valCteExp = '1'
                y.tipoDec = "int"
                p.hijos[1] = y
                t.hijos[0] = p
        elif(self.token == ":="):
            self.match(":=")
            if (t != None):
                t.hijos[0] = self.expresion()
        else:
            self.syntaxError("TOKEN NO ESPERADO -> " + self.token + " " + self.tipoToken)
            self.token = self.sigToken()
            if(self.token == "+" or self.token == "-" or self.token == "/" or self.token == "*" or
                    self.token == "<" or self.token == "<=" or self.token == ">" or self.token == ">=" or
                       self.token == "==" or self.token == "!=" or self.token == ":=" or
                        self.tipoToken == "REAL" or self.tipoToken == "INT" or self.token == "("):
                while(self.token != ";"):
                    self.token = self.sigToken()
        self.match(";")
        return t

    #EXPRESION
    def expresion(self):
        t = self.expresion_simple()
        if(self.token == "<=" or self.token == "<" or self.token == ">=" or self.token == ">" or self.token == "!=" or self.token == "=="):
            q = self.nodoExpresion("OPERADOR")
            if(t != None):
                q.hijos[0] = t
                q.OpExp = self.token
                t = q
            self.match(self.token)
            if(t != None):
                t.hijos[1] = self.expresion_simple()
        elif(self.tipoToken == "REAL" or self.tipoToken == "INT" or self.tipoToken == "IDENTIFICADOR"):
            self.syntaxError("TOKEN NO ESPERADO -> " + self.token + " " + self.tipoToken)
            self.token = self.sigToken()
        return t

    #EXPRESION_SIMPLE
    def expresion_simple(self):
        t = self.termino()
        while(self.token == "+" or self.token == "-"):
            p = self.nodoExpresion("OPERADOR")
            if(t != None):
                p.hijos[0] = t
                p.OpExp = self.token
                t = p
            self.match(self.token)
            if(t != None):
                t.hijos[1] = self.termino()
        return t

    #TERMINO
    def termino(self):
        t = self.factor()
        while (self.token == "*" or self.token == "/"):
            p = self.nodoExpresion("OPERADOR")
            if (t != None):
                p.hijos[0] = t
                p.OpExp = self.token
                t = p
            self.match(self.token)
            if(t != None):
                t.hijos[1] = self.factor()
        return t

    #FACTOR
    def factor(self):
        t = None
        if(self.token == "("):
            self.match("(")
            t = self.expresion()
            self.match(")")
        elif(self.tipoToken == "REAL" or self.tipoToken == "INT"):
            t = self.nodoExpresion(self.tipoToken)
            t.valCteExp = self.token
            self.token = self.sigToken()
        elif(self.tipoToken == "IDENTIFICADOR"):
            t = self.nodoExpresion("IDENTIFICADOR")
            t.nomIdExp = self.token
            self.token = self.sigToken()
        else:
            self.syntaxError("TOKEN NO ESPERADO -> " + self.token + " " + self.tipoToken)
            #imprimeToken(token, tipoToken)
            self.token = self.sigToken()
        return t

#IMPRIMIR ARBOL
    def imprime_arbol(self, arbol, tabulaciones):
        tabulaciones = tabulaciones + 1
        while (arbol != None):
            self.imprime_espacios(tabulaciones)
            if (arbol.nomIdExp == "main"):
                self.archivo_codigo.write("PROGRAMA\n")
            elif (arbol.tipoNodo == "SENTENCIA"):
                if (arbol.tipoSen == "if"):
                    self.archivo_codigo.write("If\n")
                elif (arbol.tipoSen == "repeat"):
                    self.archivo_codigo.write("Do\n")
                elif (arbol.tipoSen == ":="):
                    self.archivo_codigo.write("Asignacion a variable: " + str(arbol.nomIdExp) + "\n")
                elif (arbol.tipoSen == "cin"):
                    self.archivo_codigo.write("Lectura variable: " + str(arbol.nomIdExp) + "\n")
                elif (arbol.tipoSen == "cout"):
                    self.archivo_codigo.write("Escritura\n")
                elif (arbol.tipoSen == "bloque"):
                    self.archivo_codigo.write("Bloque: \n")
                elif (arbol.tipoSen == "while"):
                    self.archivo_codigo.write("While: \n")
                else:
                    self.archivo_codigo.write("Nodo de tipo SENTENCIA, DESCONOCIDO\n")
            elif (arbol.tipoNodo == "EXPRESION"):
                if (arbol.tipoExp == "OPERADOR"):
                    self.archivo_codigo.write("Operador: " + str(arbol.OpExp) + "\n")
                elif (arbol.tipoExp == "REAL" or arbol.tipoExp == "INT"):
                    self.archivo_codigo.write("Constante: " + str(arbol.valCteExp) + "\n")
                elif (arbol.tipoExp == "IDENTIFICADOR"):
                    self.archivo_codigo.write("Id: " + str(arbol.nomIdExp) + "\n")
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
                self.imprime_arbol(arbol.hijos[i],tabulaciones)
            arbol = arbol.hermanos
        tabulaciones = tabulaciones -1

    # IMPRIME ESPACIOS EN ARBOL
    def imprime_espacios(self, tabulaciones):
        for i in range(tabulaciones):
            self.archivo_codigo.write(" ")

    def cierra_archivos(self):
        self.archivo_codigo.close()
        self.archivo_errores.close()