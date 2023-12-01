#Estructura de la lista de lineas
class LineList:
    def __init__(self):
        self.noLine=None  #Número de la linea
        self.next=None    #Referencia al sig. Nodo de la lista de lineas

#Estructura tabla HASH
class regHash:
    def __init__(self):
        self.name=None #Nombre del ID
        self.lines=None #Lista de lineas
        self.memLoc=None #Localizacion en memoria
        self.next=None #Referencia al sig. Nodo del registro
        self.type=None #Tipo de la variable
        self.value=None #Valor de la variable

#Crea el la tabla
class TablaHash:
    def __init__(self):
        self.SIZE = 211
        self.SHIFT = 4
        self.archivoTabla = open("TablaHash.txt", "w")
        self.hashTable = []
        for i in range(self.SIZE):
            self.hashTable.append(None)

    #Funcion HASH
    def hashKey(self,key):
        temp=0
        tam=len(key)
        pos=0
        while(pos<tam):
            temp=  ((temp << self.SHIFT) + ord(key[pos])) % self.SIZE
            pos=pos+1
        return temp

    #Inserta o actualiza la variable en la Tabla Hash
    def insert(self,type,name,value,noLine,loc):
        h= self.hashKey(name)
        l= self.hashTable[h]
        while (l!=None and name != l.name):
            l=l.next
        if(l==None): #Cuando la variable no esta en la tabla
            l = regHash()
            l.name = name
            l.lines = LineList()
            l.lines.noLine = noLine
            l.lines.next = None
            l.memLoc=loc
            l.type=type
            if(value==None):
                l.value=0
            else:
                l.value=value
            l.next = self.hashTable[h]
            self.hashTable[h] = l
        else: #Cuando la variable si esta en la tabla
            t = l.lines
            while t.next != None:
                t=t.next
            t.next= LineList()
            t.next.noLine= noLine
            l.value = value
            t.next.next=None

    #Busca la variable en la tabla por Nombre
    def search(self,name):
        h= self.hashKey(name)
        l= regHash()
        l= self.hashTable[h]
        while(l!=None and name!=l.name):
            l=l.next
        if(l==None):
            return -1
        else:
            return l.memLoc

    #Guarda la tabla en un archivo
    def printTableFile(self):
        for i in range(self.SIZE):
            if(self.hashTable[i] != None):
                l = self.hashTable[i]
                while (l != None):
                    t= l.lines
                    self.archivoTabla.write(str(l.type)+'\t'+str(l.name)+'\t'+str(l.value)+'\t'+str(l.memLoc)+'\t')
                    # Recorre la lista de las lineas
                    while(t!=None):
                        if (t.next == None):
                            self.archivoTabla.write(str(t.noLine))
                        else:
                            self.archivoTabla.write(str(t.noLine) + ',')
                        t=t.next
                    self.archivoTabla.write('\n')
                    l = l.next
        self.archivoTabla.close()
