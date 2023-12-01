class code:
    def __init__(self):
        self.emitLoc = 0
        self.highEmitLoc = 0
        self.pc = 7 #Program counter
        self.mp = 6 #Memory Pointer, apunta a la punta de la memoria
        self.gp = 5 #Global Pointer, apunta al final de la memoria para la variable global storage
        self.ac = 0 #Acumulador
        self.ac1 = 1 #Segundo acumulador
        self.archivo = open("Code.txt", "w")
        self.archivo2 = open("readToTM.txt", "w")
        self.TraceCode = False

    def emitComment(self,msg): #Imprime comentario en el archivo code
        if(self.TraceCode):
            self.archivo.write(str(msg) + "\n")

    def emitRO(self, op, r, s, t, msg): #Emite una instrucción de sólo 1 registro
        #op = nemónico, r=registro target, s=primera fuente, t=segunda fuente, msg=comentario que va a ser impreso
        self.archivo.write(str(self.emitLoc) + ": " + str(op) + " " + str(r)+ "," + str(s) + "," + str(t)+ " ")
        self.archivo2.write(str(self.emitLoc) + '\t' + str(op) + '\t' + str(r) + '\t' + str(s) + '\t' + str(t))
        self.emitLoc = self.emitLoc + 1
        if(op == "IN"):
            self.archivo.write("\t" + str(msg))
            self.archivo2.write("\t" + str(msg))
        self.archivo.write("\n")
        self.archivo2.write("\n")
        if(self.highEmitLoc < self.emitLoc):
            self.highEmitLoc = self.emitLoc

    def emitRM(self, op, r, d, s, msg): #Emite instrucciones de un registro a memoria
        # op = nemónico, r=registro target, d=desplazamiento, s=registro base, msg=comentario que va a ser impreso
        self.archivo.write(str(self.emitLoc) + ": " + str(op) + " " + str(r) + "," + str(d) + ",(" + str(s) + ") ")
        self.archivo2.write(str(self.emitLoc) + '\t' + str(op) + '\t' + str(r) + '\t' + str(d) + '\t' + str(s))
        self.emitLoc = self.emitLoc + 1
        if (self.TraceCode):
            self.archivo.write("\t" + str(msg))
            self.archivo2.write("\t" + str(msg))
        self.archivo.write("\n")
        self.archivo2.write("\n")
        if (self.highEmitLoc < self.emitLoc):
            self.highEmitLoc = self.emitLoc

    def emitSkip(self, howMany): #Se brinca "howMany" locaciones de código para después regresar. También regresa la posicion actual
        i = self.emitLoc
        self.emitLoc += howMany
        if (self.highEmitLoc < self.emitLoc):
            self.highEmitLoc = self.emitLoc
        return i

    def emitBackup(self, loc): #Respalda la locacion
        #loc = Locación que se saltó anteriormente
        if(loc > self.highEmitLoc):
            self.emitComment("BUG in emitBackup")
        self.emitLoc = loc

    def emitRestore(self): #Restaura la posición actual del código a la posición más alta previamente no emitida
        self.emitLoc = self.highEmitLoc

    def emitRM_Abs(self, op, r, a, msg): #Convierte una referencia absoluta en una referencia a un contador de programa (pc) relativo cuando emite una instruccion de registro a memoria
        # op = nemónico, r=registro target, a=locacion absoluta de memoria, msg=comentario que va a ser impreso
        self.archivo.write(str(self.emitLoc) + ": " + str(op) + " " + str(r) + ", " + str(a-(self.emitLoc+1)) + ", (" + str(self.pc) + ") ")
        self.archivo2.write(str(self.emitLoc) + '\t' + str(op) + '\t' + str(r) + '\t' + str(a-(self.emitLoc+1)) + '\t' + str(self.pc))
        self.emitLoc = self.emitLoc + 1
        if (self.TraceCode):
            self.archivo.write("\t" + str(msg))
            self.archivo2.write("\t" + str(msg))
        self.archivo.write("\n")
        self.archivo2.write("\n")
        if (self.highEmitLoc < self.emitLoc):
            self.highEmitLoc = self.emitLoc

    def cerrarArchivos(self):
        self.archivo.close()