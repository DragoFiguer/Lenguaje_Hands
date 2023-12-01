import sys
import os.path as path

archivo = sys.argv[1]
if path.exists(archivo):
    print("EXISTE ARCHIVO")
else:
    print("NO EXISTE ARCHIVO")
archivo = open(archivo, "r")
archivo.seek(0)
archivo_tokens = open("Tokens.txt", "w")
archivo_tokens.close()
archivo_errores = open("Errores.txt", "w")
archivo_errores.close()
palabras_reservadas = ["main", "if", "then", "else", "end", "do", "while", "repeat", "until", "cin", "cout", "real", "int", "boolean", "break"]
lin = 1
tokens = []
tipo_lexema = []
comentario_ban = 0
comentario = ""
for linea in archivo:
    cadena = linea
    lexema = ""
    pos_cad = 0
    while pos_cad < len(cadena):
        if (cadena[pos_cad] == '\t' or cadena[pos_cad] == '\n' or cadena[pos_cad] == ' ') and comentario_ban == 0:
            pos_cad = pos_cad+1
        elif cadena[pos_cad].isalpha() and comentario_ban == 0:
            lexema = lexema + str(cadena[pos_cad])
            pos_cad = pos_cad+1
            if pos_cad != len(cadena):
                while cadena[pos_cad].isalnum() or cadena[pos_cad] == "_":
                    lexema = lexema + str(cadena[pos_cad])
                    pos_cad = pos_cad+1
                    if pos_cad == len(cadena):
                        break
                #FIN WHILE
            ban = 0
            for element in palabras_reservadas:
                if lexema == element:
                    tokens += [lexema]
                    tipo_lexema += ["PALABRA RESERVADA"]
                    archivo_tokens = open("Tokens.txt", "a")
                    archivo_tokens.write(lexema + "\tPALABRA RESERVADA\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                    archivo_tokens.close()
                    lexema = ""
                    ban = 1
                    break
            if ban == 0:
                tokens += [lexema]
                tipo_lexema += ["IDENTIFICADOR"]
                archivo_tokens = open("Tokens.txt", "a")
                archivo_tokens.write(lexema+"\tIDENTIFICADOR\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                archivo_tokens.close()
                lexema = ""
        elif cadena[pos_cad] == "+" and comentario_ban == 0:
            lexema = lexema + str(cadena[pos_cad])
            pos_cad = pos_cad+1
            if pos_cad < len(cadena):
                if cadena[pos_cad] == "+":
                    lexema = lexema + str(cadena[pos_cad])
                    tokens += [lexema]
                    tipo_lexema += ["OPERADOR INCREMENTO"]
                    archivo_tokens = open("Tokens.txt", "a")
                    archivo_tokens.write(lexema + "\tOPERADOR INCREMENTO\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                    archivo_tokens.close()
                    lexema = ""
                    pos_cad = pos_cad+1
                else:
                    tokens += [lexema]
                    tipo_lexema += ["OPERADOR SUMA"]
                    archivo_tokens = open("Tokens.txt", "a")
                    archivo_tokens.write(lexema + "\tOPERADOR SUMA\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                    archivo_tokens.close()
                    lexema = ""
            else:
                tokens += [lexema]
                tipo_lexema += ["OPERADOR SUMA"]
                archivo_tokens = open("Tokens.txt", "a")
                archivo_tokens.write(lexema + "\tOPERADOR SUMA\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                archivo_tokens.close()
                lexema = ""
        elif cadena[pos_cad] == "-" and comentario_ban == 0:
            lexema = lexema + str(cadena[pos_cad])
            pos_cad = pos_cad+1
            if pos_cad < len(cadena):
                if cadena[pos_cad] == "-":
                    lexema = lexema + str(cadena[pos_cad])
                    tokens += [lexema]
                    tipo_lexema += ["OPERADOR DECREMENTO"]
                    archivo_tokens = open("Tokens.txt", "a")
                    archivo_tokens.write(lexema + "\tOPERADOR DECREMENTO\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                    archivo_tokens.close()
                    lexema = ""
                    pos_cad = pos_cad+1
                else:
                    tokens += [lexema]
                    tipo_lexema += ["OPERADOR RESTA"]
                    archivo_tokens = open("Tokens.txt", "a")
                    archivo_tokens.write(lexema + "\tOPERADOR RESTA\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                    archivo_tokens.close()
                    lexema = ""
            else:
                tokens += [lexema]
                tipo_lexema += ["OPERADOR RESTA"]
                archivo_tokens = open("Tokens.txt", "a")
                archivo_tokens.write(lexema + "\tOPERADOR RESTA\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                archivo_tokens.close()
                lexema = ""
        elif cadena[pos_cad].isnumeric() and comentario_ban == 0:
            lexema = lexema + str(cadena[pos_cad])
            pos_cad = pos_cad+1
            if pos_cad != len(cadena):
                while cadena[pos_cad].isnumeric():
                    lexema = lexema + str(cadena[pos_cad])
                    pos_cad = pos_cad + 1
                    if pos_cad == len(cadena):
                        break
                # FIN WHILE
                if pos_cad < len(cadena):
                    if cadena[pos_cad] == '.':
                        lexema = lexema + str(cadena[pos_cad])
                        pos_cad = pos_cad + 1
                        if pos_cad < len(cadena):
                            if cadena[pos_cad].isnumeric():
                                while cadena[pos_cad].isnumeric():
                                    lexema = lexema + str(cadena[pos_cad])
                                    pos_cad = pos_cad + 1
                                # FIN WHILE
                                tokens += [lexema]
                                tipo_lexema += ["REAL"]
                                archivo_tokens = open("Tokens.txt", "a")
                                archivo_tokens.write(lexema + "\tREAL\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                                archivo_tokens.close()
                                lexema = ""
                            else:
                                print("ERROR LINEA " + str(lin) + " COLUMNA " + str(pos_cad+1))
                                archivo_errores = open("Errores.txt", "a")
                                archivo_errores.write(
                                    "ERROR EN LA LINEA " + str(lin) + " COLUMNA " + str(pos_cad+1) + " SE ESPERABA VALOR NUMERICO\n")
                                archivo_errores.close()
                                lexema = ""
                        else:
                            print("ERROR LINEA " + str(lin) + " COLUMNA " + str(pos_cad + 1))
                            archivo_errores = open("Errores.txt", "a")
                            archivo_errores.write(
                                "ERROR EN LA LINEA " + str(lin) + " COLUMNA " + str(
                                    pos_cad + 1) + " SE ESPERABA VALOR NUMERICO\n")
                            archivo_errores.close()
                            lexema = ""
                    else:
                        tokens += [lexema]
                        tipo_lexema += ["INT"]
                        archivo_tokens = open("Tokens.txt", "a")
                        archivo_tokens.write(lexema + "\tINT\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                        archivo_tokens.close()
                        lexema = ""
                else:
                    tokens += [lexema]
                    tipo_lexema += ["INT"]
                    archivo_tokens = open("Tokens.txt", "a")
                    archivo_tokens.write(lexema + "\tINT\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                    archivo_tokens.close()
                    lexema = ""
            else:
                tokens += [lexema]
                tipo_lexema += ["INT"]
                archivo_tokens = open("Tokens.txt", "a")
                archivo_tokens.write(lexema + "\tINT\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                archivo_tokens.close()
                lexema = ""
        elif cadena[pos_cad] == '<' and comentario_ban == 0:
            lexema = lexema + str(cadena[pos_cad])
            pos_cad = pos_cad + 1
            if pos_cad < len(cadena):
                if cadena[pos_cad] == '=':
                    lexema = lexema + str(cadena[pos_cad])
                    tokens += [lexema]
                    tipo_lexema += ["OPERADOR MENOR IGUAL QUE"]
                    archivo_tokens = open("Tokens.txt", "a")
                    archivo_tokens.write(lexema + "\tOPERADOR MENOR IGUAL QUE\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                    archivo_tokens.close()
                    lexema = ""
                    pos_cad = pos_cad + 1
                else:
                    tokens += [lexema]
                    tipo_lexema += ["OPERADOR MENOR QUE"]
                    archivo_tokens = open("Tokens.txt", "a")
                    archivo_tokens.write(lexema + "\tOPERADOR MENOR QUE\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                    archivo_tokens.close()
                    lexema = ""
            else:
                tokens += [lexema]
                tipo_lexema += ["OPERADOR MENOR QUE"]
                archivo_tokens = open("Tokens.txt", "a")
                archivo_tokens.write(lexema + "\tOPERADOR MENOR QUE\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                archivo_tokens.close()
                lexema = ""
        elif cadena[pos_cad] == '>' and comentario_ban == 0:
            lexema = lexema + str(cadena[pos_cad])
            pos_cad = pos_cad + 1
            if pos_cad < len(cadena):
                if cadena[pos_cad] == '=':
                    lexema = lexema + str(cadena[pos_cad])
                    tokens += [lexema]
                    tipo_lexema += ["OPERADOR MAYOR IGUAL QUE"]
                    archivo_tokens = open("Tokens.txt", "a")
                    archivo_tokens.write(lexema + "\tOPERADOR MAYOR IGUAL QUE\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                    archivo_tokens.close()
                    lexema = ""
                    pos_cad = pos_cad + 1
                else:
                    tokens += [lexema]
                    tipo_lexema += ["OPERADOR MAYOR QUE"]
                    archivo_tokens = open("Tokens.txt", "a")
                    archivo_tokens.write(lexema + "\tOPERADOR MAYOR QUE\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                    archivo_tokens.close()
                    lexema = ""
            else:
                tokens += [lexema]
                tipo_lexema += ["OPERADOR MAYOR QUE"]
                archivo_tokens = open("Tokens.txt", "a")
                archivo_tokens.write(lexema + "\tOPERADOR MAYOR QUE\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                archivo_tokens.close()
                lexema = ""
        elif cadena[pos_cad] == '=' and comentario_ban == 0:
            lexema = lexema + str(cadena[pos_cad])
            pos_cad = pos_cad + 1
            if pos_cad < len(cadena):
                if cadena[pos_cad] == '=':
                    lexema = lexema + str(cadena[pos_cad])
                    tokens += [lexema]
                    tipo_lexema += ["OPERADOR COMPARACION"]
                    archivo_tokens = open("Tokens.txt", "a")
                    archivo_tokens.write(lexema + "\tOPERADOR COMPARACION\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                    archivo_tokens.close()
                    lexema = ""
                    pos_cad = pos_cad + 1
                else:
                    print("ERROR LINEA " + str(lin) + " COLUMNA " + str(pos_cad))
                    archivo_errores = open("Errores.txt", "a")
                    archivo_errores.write(
                        "ERROR EN LA LINEA " + str(lin) + " COLUMNA " + str(pos_cad) + " SE ESPERABA SIGNO =\n")
                    archivo_errores.close()
                    lexema = ""
            else:
                print("ERROR LINEA " + str(lin) + " COLUMNA " + str(pos_cad))
                archivo_errores = open("Errores.txt", "a")
                archivo_errores.write(
                    "ERROR EN LA LINEA " + str(lin) + " COLUMNA " + str(pos_cad) + " SE ESPERABA SIGNO =\n")
                archivo_errores.close()
                lexema = ""
        elif cadena[pos_cad] == '!' and comentario_ban == 0:
            lexema = lexema + str(cadena[pos_cad])
            pos_cad = pos_cad + 1
            if pos_cad < len(cadena):
                if cadena[pos_cad] == '=':
                    lexema = lexema + str(cadena[pos_cad])
                    tokens += [lexema]
                    tipo_lexema += ["OPERADOR DIFERENTE QUE"]
                    archivo_tokens = open("Tokens.txt", "a")
                    archivo_tokens.write(lexema + "\tOPERADOR DIFERENTE QUE\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                    archivo_tokens.close()
                    lexema = ""
                    pos_cad = pos_cad + 1
                else:
                    print("ERROR LINEA " + str(lin) + " COLUMNA " + str(pos_cad+1))
                    archivo_errores = open("Errores.txt", "a")
                    archivo_errores.write(
                        "ERROR EN LA LINEA " + str(lin) + " COLUMNA " + str(pos_cad+1) + " SE ESPERABA SIGNO =\n")
                    archivo_errores.close()
                    lexema = ""
            else:
                print("ERROR LINEA " + str(lin) + " COLUMNA " + str(pos_cad+1))
                archivo_errores = open("Errores.txt", "a")
                archivo_errores.write(
                    "ERROR EN LA LINEA " + str(lin) + " COLUMNA " + str(pos_cad+1) + " SE ESPERABA SIGNO =\n")
                archivo_errores.close()
                lexema = ""
        elif cadena[pos_cad] == ':' and comentario_ban == 0:
            lexema = lexema + str(cadena[pos_cad])
            pos_cad = pos_cad + 1
            if pos_cad < len(cadena):
                if cadena[pos_cad] == '=':
                    lexema = lexema + str(cadena[pos_cad])
                    tokens += [lexema]
                    tipo_lexema += ["OPERADOR ASIGNACION"]
                    archivo_tokens = open("Tokens.txt", "a")
                    archivo_tokens.write(lexema + "\tOPERADOR ASIGNACION\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                    archivo_tokens.close()
                    lexema = ""
                    pos_cad = pos_cad + 1
                else:
                    print("ERROR LINEA " + str(lin) + " COLUMNA " + str(pos_cad+1))
                    archivo_errores = open("Errores.txt", "a")
                    archivo_errores.write(
                        "ERROR EN LA LINEA " + str(lin) + " COLUMNA " + str(pos_cad+1) + " SE ESPERABA SIGNO =\n")
                    archivo_errores.close()
                    lexema = ""
            else:
                print("ERROR LINEA " + str(lin) + " COLUMNA " + str(pos_cad+1))
                archivo_errores = open("Errores.txt", "a")
                archivo_errores.write(
                    "ERROR EN LA LINEA " + str(lin) + " COLUMNA " + str(pos_cad+1) + " SE ESPERABA SIGNO =\n")
                archivo_errores.close()
                lexema = ""
        elif cadena[pos_cad] == '*' and comentario_ban == 0:
            lexema = lexema + str(cadena[pos_cad])
            tokens += [lexema]
            tipo_lexema += ["OPERADOR MULTIPLICACION"]
            archivo_tokens = open("Tokens.txt", "a")
            archivo_tokens.write(lexema + "\tOPERADOR MULTIPLICACION\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
            archivo_tokens.close()
            lexema = ""
            pos_cad = pos_cad + 1
        elif cadena[pos_cad] == '%' and comentario_ban == 0:
            lexema = lexema + str(cadena[pos_cad])
            tokens += [lexema]
            tipo_lexema += ["SIMBOLO PORCIENTO"]
            archivo_tokens = open("Tokens.txt", "a")
            archivo_tokens.write(lexema + "\tSIMBOLO PORCIENTO\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
            archivo_tokens.close()
            lexema = ""
            pos_cad = pos_cad + 1
        elif cadena[pos_cad] == ',' and comentario_ban == 0:
            lexema = lexema + str(cadena[pos_cad])
            tokens += [lexema]
            tipo_lexema += ["SIMBOLO COMA(,)"]
            archivo_tokens = open("Tokens.txt", "a")
            archivo_tokens.write(lexema + "\tSIMBOLO COMA(,)\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
            archivo_tokens.close()
            lexema = ""
            pos_cad = pos_cad + 1
        elif cadena[pos_cad] == ';' and comentario_ban == 0:
            lexema = lexema + str(cadena[pos_cad])
            tokens += [lexema]
            tipo_lexema += ["SIMBOLO PUNTO Y COMA(;)"]
            archivo_tokens = open("Tokens.txt", "a")
            archivo_tokens.write(lexema + "\tSIMBOLO PUNTO Y COMA(;)\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
            archivo_tokens.close()
            lexema = ""
            pos_cad = pos_cad + 1
        elif cadena[pos_cad] == '(' and comentario_ban == 0:
            lexema = lexema + str(cadena[pos_cad])
            tokens += [lexema]
            tipo_lexema += ["PARENTESIS QUE ABRE"]
            archivo_tokens = open("Tokens.txt", "a")
            archivo_tokens.write(lexema + "\tPARENTESIS QUE ABRE\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
            archivo_tokens.close()
            lexema = ""
            pos_cad = pos_cad + 1
        elif cadena[pos_cad] == ')' and comentario_ban == 0:
            lexema = lexema + str(cadena[pos_cad])
            tokens += [lexema]
            tipo_lexema += ["PARENTESIS QUE CIERRA"]
            archivo_tokens = open("Tokens.txt", "a")
            archivo_tokens.write(lexema + "\tPARENTESIS QUE CIERRA\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
            archivo_tokens.close()
            lexema = ""
            pos_cad = pos_cad + 1
        elif cadena[pos_cad] == '{' and comentario_ban == 0:
            lexema = lexema + str(cadena[pos_cad])
            tokens += [lexema]
            tipo_lexema += ["SIMBOLO LLAVE QUE ABRE"]
            archivo_tokens = open("Tokens.txt", "a")
            archivo_tokens.write(lexema + "\tSIMBOLO LLAVE QUE ABRE\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
            archivo_tokens.close()
            lexema = ""
            pos_cad = pos_cad + 1
        elif cadena[pos_cad] == '}' and comentario_ban == 0:
            lexema = lexema + str(cadena[pos_cad])
            tokens += [lexema]
            tipo_lexema += ["SIMBOLO LLAVE QUE CIERRA"]
            archivo_tokens = open("Tokens.txt", "a")
            archivo_tokens.write(lexema + "\tSIMBOLO LLAVE QUE CIERRA\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
            archivo_tokens.close()
            lexema = ""
            pos_cad = pos_cad + 1
        elif cadena[pos_cad] == '/' and comentario_ban == 0:
            lexema = lexema + str(cadena[pos_cad])
            comentario = comentario + str(cadena[pos_cad])
            pos_cad = pos_cad+1
            if pos_cad == len(cadena):
                break
            if cadena[pos_cad] == '/':
                lexema = ""
                comentario = comentario + str(cadena[pos_cad])
                pos_cad = pos_cad+1
                while cadena[pos_cad] != '\n':
                    comentario = comentario + str(cadena[pos_cad])
                    pos_cad = pos_cad+1
                print("COMENTARIO DE UNA LINEA: " + comentario)
                comentario = ""
            elif cadena[pos_cad] == '*':
                lexema = ""
                comentario = comentario + str(cadena[pos_cad])
                pos_cad = pos_cad+1
                comentario_ban = 1
            else:
                comentario = ""
                tokens += [lexema]
                tipo_lexema += ["OPERADOR DIVISION"]
                archivo_tokens = open("Tokens.txt", "a")
                archivo_tokens.write(lexema + "\tOPERADOR DIVISION\t" + str(lin) + "\t" + str(
                                    pos_cad + 1) + "\n")
                archivo_tokens.close()
                lexema = ""
        elif comentario_ban == 1:
            comentario = comentario + str(cadena[pos_cad])
            posc = len(comentario)
            pos_cad = pos_cad+1
            fin = 0
            if comentario[posc-1] == '/':
                if comentario[posc-2] == '*':
                    fin = 1
            if fin == 1:
                print("COMENTARIO MULTILINEA: " + comentario)
                comentario = ""
                comentario_ban = 0
                fin = 0
        else:
            print("ERROR LINEA " + str(lin) + " COLUMNA " + str(pos_cad+1))
            print(cadena[pos_cad] + "\n")
            archivo_errores = open("Errores.txt", "a")
            archivo_errores.write(
                "ERROR EN LA LINEA " + str(lin) + " COLUMNA " + str(pos_cad+1) + " SIMBOLO ENCONTRADO -> " + cadena[pos_cad] + "\n")
            archivo_errores.close()
            lexema = ""
            pos_cad = pos_cad + 1
    #FIN PRIMER WHILE
    lin = lin+1
archivo_tokens = open("Tokens.txt", "a")
archivo_tokens.write("ENDFILE\t0\t0\t0")
archivo_tokens.close()
archivo.close()
if comentario_ban == 1:
    print("COMENTARIO MULTILINEA SIN CERRAR(SE LLEGO A FIN DE ARCHIVO): " + comentario)
    comentario = ""
#i = 0
#while i < len(tokens):
 #   print(tokens[i] + " --> " + tipo_lexema[i] + "\n")
  #  i = i+1
