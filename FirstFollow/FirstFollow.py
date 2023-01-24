# -*- coding: utf-8 -*-
"""FirstFollow

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Pm_dAqxsTG5QSJrEw2U0hqxXjIFHRAPS
"""

# Calculando First's y Follow's 
# Diana Estefania Ortiz Ledesma 
# A01209403

from Token import Token

class Lexer:

    # Constructor 
    def __init__(self):
        
        # Terminales
        self.terminal = {}
        # No terminales
        self.noterminal = {}  
        # Palabras reservadas   
        self.reserved = {}  

        self.arrow = False 
        self.firstL = True
        self.origin = None  
        self.previous = None  
        self.last = False  
        self.setReserved()

    # Definir las palabras reservadas que tiene el lexer
    def setReserved(self):    
        self.reserved['->'] = 0
        self.reserved['\' \''] = 1

    # Escanea la línea para todos los tokens 
    def scan(self, entrada):
        self.arrow = False
        self.previous = None
        self.last = False
        token = None
        epsilon = 0  

        # Recorre la línea de entrada carácter por carácter
        for c in entrada:
          # Acciones a realizar si es un epsilon 
            if 0 < epsilon:
                if epsilon == 1:
                    if c.isspace():
                        epsilon = 2
                        token += ' '
                        continue
                    else:
                        epsilon = 0
                
                elif epsilon == 2:
                    if c == '\'':
                        epsilon = 3
                        token += '\''
                        continue
                    else:
                        epsilon = 0
                        self.saveToken('\'')
                        token = None
                
                elif epsilon == 3:
                    if c.isspace():
                        epsilon = 0
                        self.saveToken(token)
                        token = None
                        continue
                    else:
                        epsilon = 0
                        self.saveToken('\'')
                        token = '\''

            # Si el carácter es un espacio se guarda el token
            if c.isspace():
                self.saveToken(token)
                token = None  
                continue

            # Si el caracter es un numero se guarda como numero
            if c.isnumeric():
                if token == None:
                    token = 0
              
                elif isinstance(token, str):
                    token += c
                    continue

                token = (token*10)+int(c)

            # Si el caracter es una letra se guarda como string 
            elif c.isalpha():
                if token == None:
                    token = ''
                
                elif isinstance(token, int):
                    token = str(token)
                
                token += c

            # Si el caracter es un simbolo, revisa si es un epsilon y se guarda
            elif c.isascii():
                if token == None:
                    if c == '\'':
                        epsilon = 1
                        token = '\''
                        continue
                    token = ''
               
                elif isinstance(token, int):
                    token = str(token)
                
                token += c
        
        # Guardar ultimo token
        self.last = True
        self.saveToken(token)
        # Terminar produccion
        self.noterminal[self.origin].endProduction()

    # Guarda el token en terminal o no terminal
    def saveToken(self, token):
        # Checa si esta vacio
        if token == None:
            return

        # Checa si el token es una palabra reservada 
        # Revisa que tipo 
        # Si es flecha, se guarda lo demás como no terminal 
        # Si es epsilon, se guarda como produccion
        t = self.reserved.get(token)
        if t != None:
            if t == 0:
                self.arrow = True
                self.firstL = False  
            
            if t == 1:
                self.noterminal[self.origin].addProduction(token)
            return

        t = self.terminal.get(token)
        n = self.noterminal.get(token)

        # Si es flecha, se guarda como terminal
        if self.arrow == True:
            if n == None:
                self.terminal[token] = Token(token, True, self.firstL)
            
            self.noterminal[self.origin].addProduction(token)
            
            if n == None:
                self.terminal[token].addOrigin(self.origin)
            else:
                self.noterminal[token].addOrigin(self.origin)
          
            if self.previous != None:
                t = self.terminal.get(self.previous)
                if t == None:
                    self.noterminal[self.previous].addFollow(token)
                else:
                    self.terminal[self.previous].addFollow(token)
            
            if self.last:
                if n == None:
                    self.terminal[token].addFollow(None)
                else:
                    self.noterminal[token].addFollow(None)
            
            self.previous = token
            return

        # Si no es flecha, se crea un token
        if t == None:
            t = Token(token, False, self.firstL)
        else:
            self.terminal.pop(token)
       
        if n == None:
            self.noterminal[token] = t
            self.noterminal[token].setTerminal(False)
        self.origin = token

    # Calcular first y follows
    # Calcular y mostrar si es LL1
    # Imprimir first y follows 
    def printFirstsFollows(self):

        tokens = {**self.noterminal, **self.terminal, **self.reserved}
  
        for token in self.noterminal.values():
            print(token.getValue(),
                  " => FIRST ={",
                  token.getFirsts(tokens),
                  "}, FOLLOW = {",
                  token.getFollows(tokens), "}", sep='')
        print("LL(1)? ", end='')
        
        for token in self.noterminal.values():
            if token.isLL(tokens) == False:
                print('No')
                return
        print('Yes')
        
    # Imprimir todos los terminales y no terminales que tiene el lexer
    def toString(self):
      
        print('Terminal:', end='')
        tokens = list(self.terminal.values())
        for i in range(tokens.__len__()):
            if i != 0:
                print(',', end='')
            print(' '+str(tokens[i].getValue()), end='')

        print('\nNon terminal:', end='')
        tokens = list(self.noterminal.values())
        for i in range(tokens.__len__()):
            if i != 0:
                print(',', end='')
            print(' '+str(tokens[i].getValue()), end='')
        print('\n')

num = int(input())  
lexer = Lexer()  

for n in range(num): 
    lexer.scan(input()) 

lexer.printFirstsFollows()