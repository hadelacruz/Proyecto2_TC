"""
Implementación del algoritmo CYK (Cocke-Younger-Kasami)
Usa programación dinámica para determinar si una frase pertenece al lenguaje
"""

import time

class CYKAlgorithm:
    def __init__(self, productions, terminals, non_terminals, start_symbol):
        self.productions = productions
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.start_symbol = start_symbol
        self.table = None
        self.backtrack = None
        
    def parse(self, sentence):
        """
        Aplica el algoritmo CYK a una frase
        Retorna: (pertenece, tiempo, tabla, backtrack)
        """
        print(f"\n🔍 Analizando: '{sentence}'")
        
        start_time = time.time()
        
        # Tokenizar la frase
        words = sentence.lower().split()
        n = len(words)
        
        print(f"   Palabras: {words}")
        print(f"   Longitud: {n}")
        
        # Inicializar tabla de programación dinámica
        # table[i][j] contiene el conjunto de no-terminales que pueden derivar
        # la subcadena desde la posición i con longitud j+1
        self.table = [[set() for _ in range(n)] for _ in range(n)]
        
        # Inicializar tabla de backtracking para construir el árbol
        self.backtrack = [[{} for _ in range(n)] for _ in range(n)]
        
        # Paso 1: Llenar la diagonal (subcadenas de longitud 1)
        print("\n   📊 Llenando tabla CYK (programación dinámica)...")
        for i in range(n):
            word = words[i]
            # Buscar producciones que deriven este terminal
            for nt, prods in self.productions.items():
                for prod in prods:
                    if len(prod) == 1 and prod[0] == word:
                        self.table[i][0].add(nt)
                        self.backtrack[i][0][nt] = ('terminal', word)
        
        # Paso 2: Llenar el resto de la tabla (subcadenas de longitud > 1)
        for length in range(2, n + 1):  # Longitud de la subcadena
            for i in range(n - length + 1):  # Posición inicial
                j = length - 1  # Índice en la tabla
                
                # Probar todas las particiones posibles
                for k in range(length - 1):  # Punto de partición
                    # Obtener los conjuntos de no-terminales de las dos partes
                    left_set = self.table[i][k]
                    right_set = self.table[i + k + 1][j - k - 1]
                    
                    # Buscar producciones A -> BC donde B está en left_set y C en right_set
                    for nt, prods in self.productions.items():
                        for prod in prods:
                            if len(prod) == 2:
                                B, C = prod
                                if B in left_set and C in right_set:
                                    self.table[i][j].add(nt)
                                    # Guardar información para backtracking
                                    self.backtrack[i][j][nt] = ('split', B, C, i, k, j)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Verificar si el símbolo inicial está en la celda superior derecha
        belongs = self.start_symbol in self.table[0][n - 1]
        
        return belongs, elapsed_time, words
    
    def build_parse_tree(self, words):
        """Construye el árbol de análisis sintáctico"""
        n = len(words)
        if self.start_symbol not in self.table[0][n - 1]:
            return None
        
        return self._build_tree(self.start_symbol, 0, n - 1)
    
    def _build_tree(self, symbol, i, j):
        """Construye recursivamente el árbol de análisis"""
        if symbol not in self.backtrack[i][j]:
            return None
        
        info = self.backtrack[i][j][symbol]
        
        if info[0] == 'terminal':
            # Nodo hoja (terminal)
            return {'symbol': symbol, 'terminal': info[1], 'children': []}
        else:
            # Nodo interno (producción A -> BC)
            _, B, C, pos_i, k, pos_j = info
            
            left_child = self._build_tree(B, pos_i, k)
            right_child = self._build_tree(pos_i + k + 1, pos_j - k - 1)
            
            return {
                'symbol': symbol,
                'children': [left_child, right_child]
            }
    
    def display_table(self, words):
        """Muestra la tabla de programación dinámica"""
        n = len(words)
        print("\n" + "=" * 80)
        print("TABLA DE PROGRAMACIÓN DINÁMICA (CYK)")
        print("=" * 80)
        
        # Mostrar tabla en formato triangular
        for j in range(n - 1, -1, -1):
            row = []
            for i in range(n - j):
                cell = self.table[i][j]
                if cell:
                    cell_str = "{" + ", ".join(sorted(cell)) + "}"
                else:
                    cell_str = "∅"
                row.append(cell_str)
            
            # Mostrar índices de palabras cubiertas
            if j == 0:
                indices = " | ".join([f"[{i}]" for i in range(n)])
                print(f"\n{indices}")
            
            print(f"Nivel {j + 1}: {' | '.join(row)}")
        
        # Mostrar palabras
        print(f"\nPalabras: {' | '.join(words)}")
        print("=" * 80)
    
    def print_parse_tree(self, tree, words, indent=0):
        """Imprime el árbol de análisis en formato legible"""
        if tree is None:
            return ""
        
        result = "  " * indent
        
        if 'terminal' in tree:
            result += f"({tree['symbol']} {tree['terminal']})\n"
        else:
            result += f"({tree['symbol']}\n"
            for child in tree['children']:
                if child:
                    result += self.print_parse_tree(child, words, indent + 1)
            result += "  " * indent + ")\n"
        
        return result
    
    def build_parse_tree_fixed(self, words):
        """Construye el árbol de análisis sintáctico (versión corregida)"""
        n = len(words)
        if self.start_symbol not in self.table[0][n - 1]:
            return None
        
        return self._build_tree_fixed(self.start_symbol, 0, n - 1, words)
    
    def _build_tree_fixed(self, symbol, i, j, words):
        """Construye recursivamente el árbol de análisis (versión corregida)"""
        if i > j or i < 0 or j >= len(words):
            return None
            
        if symbol not in self.backtrack[i][j]:
            return None
        
        info = self.backtrack[i][j][symbol]
        
        if info[0] == 'terminal':
            # Nodo hoja (terminal)
            return {'symbol': symbol, 'terminal': info[1], 'children': []}
        else:
            # Nodo interno (producción A -> BC)
            _, B, C, pos_i, k, pos_j = info
            
            # Calcular índices correctos para los hijos
            left_end = k
            right_start = pos_i + k + 1
            right_end = pos_j - k - 1
            
            # Validar índices
            if left_end < 0 or right_end < 0 or right_start >= len(words):
                return {'symbol': symbol, 'children': []}
            
            left_child = self._build_tree_fixed(B, pos_i, left_end, words)
            right_child = self._build_tree_fixed(C, right_start, right_end, words)
            
            children = []
            if left_child:
                children.append(left_child)
            if right_child:
                children.append(right_child)
            
            return {
                'symbol': symbol,
                'children': children
            }
