"""
Parser de gramáticas CFG
Lee y parsea gramáticas desde archivos de texto
"""

class GrammarParser:
    def __init__(self, filename):
        self.filename = filename
        self.productions = {}
        self.terminals = set()
        self.non_terminals = set()
        self.start_symbol = None
        
    def parse(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                
                # Ignorar líneas vacías y comentarios
                if not line or line.startswith('#'):
                    continue
                    
                # Parsear producción
                if '->' in line:
                    self._parse_production(line)
        
        # El primer no-terminal es el símbolo inicial
        if not self.start_symbol and self.non_terminals:
            self.start_symbol = 'S'
            
        return self.productions, self.terminals, self.non_terminals, self.start_symbol
    
    def _parse_production(self, line):
        parts = line.split('->')
        if len(parts) != 2:
            return
            
        left = parts[0].strip()
        right = parts[1].strip()
        
        # El lado izquierdo es un no-terminal
        self.non_terminals.add(left)
        
        # Si es el primer símbolo, es el inicial
        if self.start_symbol is None:
            self.start_symbol = left
        
        # Inicializar lista de producciones para este no-terminal
        if left not in self.productions:
            self.productions[left] = []
        
        # Procesar alternativas separadas por |
        alternatives = [alt.strip() for alt in right.split('|')]
        
        for alt in alternatives:
            # Separar los símbolos
            symbols = alt.split()
            
            # Determinar si son terminales o no-terminales
            for symbol in symbols:
                if symbol.islower() or not symbol.isalpha():
                    self.terminals.add(symbol)
                else:
                    self.non_terminals.add(symbol)
            
            # Guardar la producción
            self.productions[left].append(symbols)
    
    def display_grammar(self):
        print("=" * 60)
        print("GRAMÁTICA ORIGINAL (CFG)")
        print("=" * 60)
        print(f"Símbolo inicial: {self.start_symbol}")
        print(f"\nNo-terminales: {sorted(self.non_terminals)}")
        print(f"\nTerminales: {sorted(self.terminals)}")
        print("\nProducciones:")
        for nt in sorted(self.productions.keys()):
            for prod in self.productions[nt]:
                print(f"  {nt} -> {' '.join(prod)}")
        print("=" * 60)
