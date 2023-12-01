class OPCLASS:
    def __init__(self):
        self.opclRR=0
        self.opclRM=1
        self.opclRA=2

class OPCODE:
    def __init__(self):
        # Instrucciones RR
        self.opHALT=0
        self.opIN=1
        self.opOUT=2
        self.opADD=3
        self.opSUB=4
        self.opMUL=5
        self.opDIV=6
        self.opRRLim=7
        # Instrucciones RM
        self.opLD=8
        self.opST=9
        self.opRMLim=10
        # Instrucciones RA
        self.opLDA=11
        self.opLDC=12
        self.opJLT=13
        self.opJLE=14
        self.opJGT=15
        self.opJGE=16
        self.opJEQ=17
        self.opJNE=18
        self.opRALim=19

class STEPRESULT:
    def __init__(self):
        self.srOKAY=0
        self.srHALT=1
        self.srIMEM_ERR=2
        self.srDMEM_ERR=3
        self.srZERODIVIDE=4

class INSTRUCTION:
    def __init__(self):
        self.iop=0
        self.iarg1=0
        self.iarg2=0
        self.iarg3=0
        self.tipoDato=""

class mt:
    def __init__(self):
        self.cont = 0
        self.IADDR_SIZE= 1024
        self.DADDR_SIZE = 1024
        self.NO_REGS=8
        self.PC_REG=7
        ###   Variables   ###
        self.iMem=[]  #tipo INSTRUCTION de tamaño IADDR_SIZE
        self.dMem = []  #tipo INT de tamaño DADDR_SIZE
        self.reg = []   #TIPO INT de tamaño NO_REGS
        self.opCodeTab=["HALT","IN","OUT","ADD","SUB","MUL","DIV","????","LD","ST","????","LDA","LDC","JLT","JLE","JGT","JGE","JEQ","JNE","????"]
        self.stepResultTab=["OK","Halted","Instruction Memory Fault","Data Memory Fault","Division by 0"]
        self.archivoLectura = open("readToTM.txt", "r")
        #self.archivoLectura = open("IDE//readToTM.txt", "r")
        for i in  range(self.IADDR_SIZE):
            self.iMem.append(INSTRUCTION())
        for i in range(self.NO_REGS):
            self.reg.append(0)
        self.dMem.append(self.DADDR_SIZE - 1)
        for i in range(self.DADDR_SIZE):
            self.dMem.append(0)
        a = OPCODE()
        for i in range(self.IADDR_SIZE):
            self.iMem[i].iop= a.opHALT
            self.iMem[i].iarg1 = 0
            self.iMem[i].iarg2 = 0
            self.iMem[i].iarg3 = 0

    def opClass (self, c ):
        a = OPCODE()
        b = OPCLASS()
        if c <= a.opRRLim :
            return (b.opclRR)
        elif c <= a.opRMLim :
            return b.opclRM
        else:
            return b.opclRA

    def error(self,msg,lineNo,instNo):
        print("Line "+ str(lineNo))
        if (instNo >= 0):
            print("(Instruction " + str(instNo)+')')
        print("   "+str(msg) + '\n')

    def getOpCode(self,opcode):
        for i in range(len(self.opCodeTab)):
            if (self.opCodeTab[i]==opcode):
                return i
        return -1

    def run(self):
        a = STEPRESULT()
        stepResult = a.srOKAY
        while stepResult == a.srOKAY:
            stepResult = self.stepTM()

    def type(self,num):
        if num.find('.') != -1:
            return float(num)
        return int (num)

    def tipoD(self,num):
        if(type(num) == int):
            return "int"
        elif(type(num) == float):
            return "real"

    def readInstructions(self):
        op = 0
        lineNo=0
        opcode= OPCODE()
        for linea in self.archivoLectura.readlines():
            lineNo=lineNo+1
            datos= linea.split('\t')
            if(len(datos) > 5):
                aux = datos[5].split("\n")
                tipoDat = aux[0]
            else:
                tipoDat = ""
            loc = int(datos[0])
            if(loc > self.IADDR_SIZE):
                self.error("Location too large"+lineNo,loc)
            op = opcode.opHALT
            if(self.getOpCode(datos[1]) == -1):
                self.error("Illegal opcode",lineNo,loc)
            else:
                op= self.getOpCode(datos[1])
            arg1 = self.type(datos[2])
            arg2 = self.type(datos[3])
            arg3 = self.type(datos[4])
            if arg1 < 0 or arg1>= self.NO_REGS:
                self.error("Bad first register",lineNo,loc)
            if op<7:
                if arg2 < 0 or arg2 >= self.NO_REGS:
                    self.error("Bad second register", lineNo, loc)
            if arg3 < 0 or arg3 >= self.NO_REGS:
                self.error("Bad third register", lineNo, loc)
            self.iMem[loc].iop = op
            self.iMem[loc].iarg1 = arg1
            self.iMem[loc].iarg2 = arg2
            self.iMem[loc].iarg3 = arg3
            self.iMem[loc].tipoDato = tipoDat

    def stepTM(self):
        pc = self.reg[self.PC_REG]
        stepResult = STEPRESULT()
        opclass =  OPCLASS()
        opcode = OPCODE()
        if((pc<0)or(pc>self.IADDR_SIZE)):
            return stepResult.srIMEM_ERR
        self.reg[self.PC_REG]= pc+1
        currentIntruction = self.iMem[pc]
        if (self.opClass(currentIntruction.iop) == opclass.opclRR):
            r = currentIntruction.iarg1
            s = currentIntruction.iarg2
            t = currentIntruction.iarg3
            tipoDato = currentIntruction.tipoDato
        elif(self.opClass(currentIntruction.iop) == opclass.opclRM):
            r = currentIntruction.iarg1
            s = currentIntruction.iarg3
            m = currentIntruction.iarg2 + self.reg[s]
            if (m < 0) or (m > self.DADDR_SIZE):
                return stepResult.srDMEM_ERR
        elif (self.opClass(currentIntruction.iop) == opclass.opclRA):
            r = currentIntruction.iarg1
            s = currentIntruction.iarg3
            m = currentIntruction.iarg2 + self.reg[s]
        #####   Instrucciones RR
        if(currentIntruction.iop == opcode.opHALT):
            print("Ejecucion finalizada\n")
            return stepResult.srHALT
        elif(currentIntruction.iop == opcode.opIN):
            print("cin>>")
            in_Line = input()
            #print(in_Line)
            val = self.type(in_Line)
            try:
                if (self.tipoD(val)==tipoDato ):
                    self.reg[r]= self.type(in_Line)
                elif(self.tipoD(val)=="int" and tipoDato=="real"):
                    self.reg[r] = float(self.type(in_Line))
                else:
                    print("cin << Illegal value")
            except:
                print("TM Error: cin << Illegal value")
                #print("TM Error: Illegal value",file=sys.stderr)
        elif(currentIntruction.iop == opcode.opOUT):
             #print(str("cout>>"+self.reg[r]))
            if(self.cont==0):
                print("cout>> ",end="")
            #print(str(self.reg[r]),end="")
            print(str(self.reg[r])+"\n", end="")
            """self.cont = self.cont + 1
            if(self.cont > 3):
                print("")
                self.cont = 0"""
        elif(currentIntruction.iop == opcode.opADD):
            self.reg[r] = self.reg[s] + self.reg[t]
        elif (currentIntruction.iop == opcode.opSUB):
            self.reg[r] = self.reg[s] - self.reg[t]
        elif (currentIntruction.iop == opcode.opMUL):
            self.reg[r] = self.reg[s] * self.reg[t]
        elif (currentIntruction.iop == opcode.opDIV):
            if (self.reg[t] != 0):
                self.reg[r] = self.reg[s] / self.reg[t]
            else:
                return stepResult.srZERODIVIDE
        ######   instrucciones RM
        elif (currentIntruction.iop == opcode.opLD):
            self.reg[r] = self.dMem[m]
        elif (currentIntruction.iop == opcode.opST):
            self.dMem[m] = self.reg[r]
        ###### instrucciones RA
        elif (currentIntruction.iop == opcode.opLDA):
            self.reg[r]= m
        elif (currentIntruction.iop == opcode.opLDC):
            self.reg[r] = currentIntruction.iarg2
        elif (currentIntruction.iop == opcode.opJLT):
            if self.reg[r]<0:
                self.reg[self.PC_REG]=m
        elif (currentIntruction.iop == opcode.opJLE):
            if self.reg[r]<=0:
                self.reg[self.PC_REG]=m
        elif (currentIntruction.iop == opcode.opJGT):
            if self.reg[r]>0:
                self.reg[self.PC_REG]=m
        elif (currentIntruction.iop == opcode.opJGE):
            if self.reg[r]>=0:
                self.reg[self.PC_REG]=m
        elif (currentIntruction.iop == opcode.opJEQ):
            if self.reg[r]==0:
                self.reg[self.PC_REG]=m
        elif (currentIntruction.iop == opcode.opJNE):
            if self.reg[r]!=0:
                self.reg[self.PC_REG]=m
        return stepResult.srOKAY



maquina = mt()
maquina.readInstructions()
maquina.run()