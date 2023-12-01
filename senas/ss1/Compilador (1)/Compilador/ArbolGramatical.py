from AnalizadorSintaxis import AnalizadorSintaxis
from AnalizadorSemantico import AnalizadorSemantico
from CodigoIntermedio import generaCI
from TablaHash import TablaHash

obj = AnalizadorSintaxis()
obj2 = AnalizadorSemantico()
print("ENTRO AL ARCHIVO")
arbol = obj.programa()
obj.imprime_arbol(arbol,-1)
print("salio imprime")
obj.cierra_archivos()
obj2.pasandoTipo(arbol)
obj2.pasandoValor(arbol)
obj2.tabla.printTableFile()
obj2.imprime_arbol_Sem(arbol,-1)
print("salio imrime 2")
obj2.cierra_archivos()
tabla = obj2.tabla
obj3 = generaCI(tabla)
obj3.codeGen(arbol.hijos[1],"Code.txt")
