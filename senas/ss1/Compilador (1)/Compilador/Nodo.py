class nodo:
    def __init__(self):
        self.hijos = [None,None,None]
        self.hermanos = None
        self.linea = 0
        self.tipoNodo = None #Sentencia,Expresion o Declaracion
        self.tipoDec = None #int float o boolean
        self.tipoSen = None # if , while , ...
        self.tipoExp = None # Id, Constante, Operador
        self.nomIdExp = None
        self.valCteExp= None
        self.OpExp = None
        self.error = None
        #self.tipoDato = None #Real, boolenano. entero