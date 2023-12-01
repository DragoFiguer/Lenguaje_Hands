from HerramientasCode import code

class generaCI:

    def __init__(self, tabla):
        self.tmpOffset = 0 #Memory offset for temps... Decrementa cada qez que un tempo es almacenado, e incrementa con es cargado otra vez
        self.code = code()
        self.tabla = tabla
        self.bbreak = False
        self.locbreak = 0

    def genStmt(self, arbol):
        p1 = None
        p2 = None
        p3 = None
        savedLoc1 = None
        savedLoc2 = None
        currentLoc = None
        loc = None
        if(arbol.tipoSen == "bloque"):
            self.cGen(arbol.hijos[0])
        elif(arbol.tipoSen == "break"):
            self.bbreak = True
            self.locbreak = self.code.emitSkip(1)
            self.code.emitComment("BREAK")
        elif(arbol.tipoSen == "if"):
            if(self.code.TraceCode):
                self.code.emitComment("-> if")
            p1 = arbol.hijos[0]
            p2 = arbol.hijos[1]
            p3 = arbol.hijos[2]
            #Generate code for test expression
            self.cGen(p1) #Genera codigo hijo 0 CONDICION
            savedLoc1 = self.code.emitSkip(1)
            self.code.emitComment("if: jump to else belongs here") #Crea etiqueta1 para caso false
            #"Then"
            self.cGen(p2) #Genra codigo para hijo 1 TRUE
            savedLoc2 = self.code.emitSkip(1)
            self.code.emitComment("if: jump to end belongs here") #Crea etiqueta2 para end
            currentLoc = self.code.emitSkip(0)
            self.code.emitBackup(savedLoc1)
            self.code.emitRM_Abs("JEQ",self.code.ac,currentLoc,"if: jmp to else") #Brinca a etiqueta1
            self.code.emitRestore()
            #"Else"
            self.cGen(p3)
            currentLoc = self.code.emitSkip(0)
            self.code.emitBackup(savedLoc2)
            self.code.emitRM_Abs("LDA",self.code.pc,currentLoc,"if: jmp to end") #Brinca a etiqueta2
            self.code.emitRestore()
            if(self.code.TraceCode):
                self.code.emitComment("<- if")
        elif(arbol.tipoSen == "while"):
            if (self.code.TraceCode):
                self.code.emitComment("-> while")
            p1 = arbol.hijos[0]
            p2 = arbol.hijos[1]
            savedLoc1 = self.code.emitSkip(0)
            # Genera codigo para la prueba
            self.cGen(p1)
            savedLoc2 = self.code.emitSkip(1)
            #True
            self.cGen(p2)  # Genra codigo para hijo 1 TRUE
            currentLoc = self.code.emitSkip(0)
            self.code.emitBackup(savedLoc2)
            self.code.emitRM_Abs("JEQ",self.code.ac,currentLoc+1,"while: jump back to test")
            if(self.bbreak):
                self.code.emitBackup(self.locbreak)
                self.code.emitRM_Abs("LDA",self.code.pc,currentLoc+1,"while: jump to end by BREAK")
                self.bbreak = False
            self.code.emitRestore()
            self.code.emitRM_Abs("LDA",self.code.pc,savedLoc1,"while: jump to end")
            if (self.code.TraceCode):
                self.code.emitComment("<- while")
        elif(arbol.tipoSen == "repeat"):
            if(self.code.TraceCode):
                self.code.emitComment("-> repeat")
            p1 = arbol.hijos[0]
            p2 = arbol.hijos[1]
            savedLoc1 = self.code.emitSkip(0)
            self.code.emitComment("repeat: jump after body comes back here")
            #Genra codigo para el cuerpo
            self.cGen(p1)
            #Genera codigo para la prueba
            self.cGen(p2)
            if(self.bbreak):
                currentLoc=self.code.emitSkip(0)
                self.code.emitBackup(self.locbreak)
                self.code.emitRM_Abs("LDA", self.code.pc, currentLoc+1, "while: jmp to end")
                self.bbreak = False
                self.code.emitRestore()
            self.code.emitRM_Abs("JEQ",self.code.ac,savedLoc1,"repeat: jmp back to body")
            if(self.code.TraceCode):
                self.code.emitComment("<- repeat")
        elif (arbol.tipoSen == ":="):
            if (self.code.TraceCode):
                self.code.emitComment("-> assign")
            #Genera codigo para rhs
            self.cGen(arbol.hijos[0])
            #Almacena valor
            loc = self.tabla.search(arbol.nomIdExp)
            self.code.emitRM("ST",self.code.ac,loc,self.code.gp,"assign: store value")
            if (self.code.TraceCode):
                self.code.emitComment("<- assign")
        elif(arbol.tipoSen == "cin"):
                self.code.emitRO("IN",self.code.ac,0,0,self.tabla.hashTable[self.tabla.hashKey(arbol.hijos[0].nomIdExp)].type)
                loc = self.tabla.search(arbol.hijos[0].nomIdExp)
                self.code.emitRM("ST", self.code.ac, loc, self.code.gp, "read: store value")
        elif(arbol.tipoSen == "cout"):
            #Genera codigo para la expresion a escribir
            self.cGen(arbol.hijos[0])
            #Ahora lo imprime
            self.code.emitRO("OUT",self.code.ac,0,0,"write ac")

    #Genera codigo en el nodo de una expresion
    def genExp(self, arbol):
        loc = 0
        p1 = None
        p2 = None
        if(arbol.tipoExp == "INT" or arbol.tipoExp == "REAL"):
            if(self.code.TraceCode):
                self.code.emitComment("-> Const")
            #Genera codigo para cargar constante
            self.code.emitRM("LDC", self.code.ac, arbol.valCteExp, 0, "load real const")
            if(self.code.TraceCode):
                self.code.emitComment("<- Const")
        elif(arbol.tipoExp == "IDENTIFICADOR"):
            if (self.code.TraceCode):
                self.code.emitComment("-> Id")
            loc = self.tabla.search(arbol.nomIdExp)
            self.code.emitRM("LD",self.code.ac,loc,self.code.gp,"load id value")
            if (self.code.TraceCode):
                self.code.emitComment("<- Id")
        elif(arbol.tipoExp == "OPERADOR"):
            if (self.code.TraceCode):
                self.code.emitComment("-> Op")
            p1 = arbol.hijos[0]
            p2 = arbol.hijos[1]
            #Genera codigo para ac = argumento izq
            self.cGen(p1)
            # Genera codigo para meter el operando izq
            self.code.emitRM("ST",self.code.ac,self.tmpOffset,self.code.mp,"op: push left")
            self.tmpOffset = self.tmpOffset - 1
            # Genera codigo para ac = argumento der
            self.cGen(p2)
            # Carga el operando izq
            self.tmpOffset = self.tmpOffset + 1
            self.code.emitRM("LD", self.code.ac1, self.tmpOffset, self.code.mp, "op: load left")
            if(arbol.OpExp == "+"):
                self.code.emitRO("ADD", self.code.ac, self.code.ac1, self.code.ac, "op +")
            elif(arbol.OpExp == "-"):
                self.code.emitRO("SUB", self.code.ac, self.code.ac1, self.code.ac, "op -")
            elif (arbol.OpExp == "*"):
                self.code.emitRO("MUL", self.code.ac, self.code.ac1, self.code.ac, "op *")
            elif (arbol.OpExp == "/"):
                self.code.emitRO("DIV", self.code.ac, self.code.ac1, self.code.ac, "op /")
            elif (arbol.OpExp == "<"):
                self.code.emitRO("SUB", self.code.ac, self.code.ac1, self.code.ac, "op <")
                self.code.emitRM("JLT", self.code.ac, 2 , self.code.pc, "br if true")
                self.code.emitRM("LDC", self.code.ac, 0 , self.code.ac, "false case")
                self.code.emitRM("LDA", self.code.pc, 1 , self.code.pc, "unconditional jmp")
                self.code.emitRM("LDC", self.code.ac, 1 , self.code.ac, "true case")
            elif (arbol.OpExp == "<="):
                self.code.emitRO("SUB", self.code.ac, self.code.ac1, self.code.ac, "op <=")
                self.code.emitRM("JLE", self.code.ac, 2 , self.code.pc, "br if true")
                self.code.emitRM("LDC", self.code.ac, 0 , self.code.ac, "false case")
                self.code.emitRM("LDA", self.code.pc, 1 , self.code.pc, "unconditional jmp")
                self.code.emitRM("LDC", self.code.ac, 1 , self.code.ac, "true case")
            elif (arbol.OpExp == ">"):
                self.code.emitRO("SUB", self.code.ac, self.code.ac1, self.code.ac, "op >")
                self.code.emitRM("JGT", self.code.ac, 2 , self.code.pc, "br if true")
                self.code.emitRM("LDC", self.code.ac, 0 , self.code.ac, "false case")
                self.code.emitRM("LDA", self.code.pc, 1 , self.code.pc, "unconditional jmp")
                self.code.emitRM("LDC", self.code.ac, 1 , self.code.ac, "true case")
            elif (arbol.OpExp == ">="):
                self.code.emitRO("SUB", self.code.ac, self.code.ac1, self.code.ac, "op >=")
                self.code.emitRM("JGE", self.code.ac, 2 , self.code.pc, "br if true")
                self.code.emitRM("LDC", self.code.ac, 0 , self.code.ac, "false case")
                self.code.emitRM("LDA", self.code.pc, 1 , self.code.pc, "unconditional jmp")
                self.code.emitRM("LDC", self.code.ac, 1 , self.code.ac, "true case")
            elif (arbol.OpExp == "=="):
                self.code.emitRO("SUB", self.code.ac, self.code.ac1, self.code.ac, "op ==")
                self.code.emitRM("JEQ", self.code.ac, 2 , self.code.pc, "br if true")
                self.code.emitRM("LDC", self.code.ac, 0 , self.code.ac, "false case")
                self.code.emitRM("LDA", self.code.pc, 1 , self.code.pc, "unconditional jmp")
                self.code.emitRM("LDC", self.code.ac, 1 , self.code.ac, "true case")
            elif (arbol.OpExp == "!="):
                self.code.emitRO("SUB", self.code.ac, self.code.ac1, self.code.ac, "op !=")
                self.code.emitRM("JNE", self.code.ac, 2 , self.code.pc, "br if true")
                self.code.emitRM("LDC", self.code.ac, 0 , self.code.ac, "false case")
                self.code.emitRM("LDA", self.code.pc, 1 , self.code.pc, "unconditional jmp")
                self.code.emitRM("LDC", self.code.ac, 1 , self.code.ac, "true case")
            else:
                self.code.emitComment("BUG: Unknown operator")
            if(self.code.TraceCode):
                self.code.emitComment("<- Op")

    #De manera recursiva  genera codigo viajando por el arbol
    def cGen(self,arbol):
        if(arbol != None):
            if(arbol.tipoNodo == "SENTENCIA"):
                self.genStmt(arbol)
            elif(arbol.tipoNodo == "EXPRESION"):
                self.genExp(arbol)
            self.cGen(arbol.hermanos)

    #FUNCION PRINCIPAL DEL GENERADOR DE CODIGO
    #Genera codigo en un archivo, mientras viaja por el arbol sintactico
    #El segundo parámetro es el nombre del archivo de codigo y es utilizado para imprimir el nombre del archivo como un comentario en el archivo
    def  codeGen(self, arbol, archivoCod):
        s = "File: "
        s += archivoCod
        self.code.emitComment("Compilacion a Codigo Intermedio")
        self.code.emitComment(s)
        #Genera preludio estandar
        self.code.emitComment("Standar prelude:")
        self.code.emitRM("LD",self.code.mp,0,self.code.ac,"load maxaddress from location 0")
        self.code.emitRM("ST", self.code.ac, 0, self.code.ac, "clear location 0")
        self.code.emitComment("End of standard prelude.")
        #Genera codigo para el programa
        self.cGen(arbol)
        #Final
        self.code.emitComment("End of execution.")
        self.code.emitRO("HALT",0,0,0,"")
        self.code.cerrarArchivos()