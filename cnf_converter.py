"""
Conversor de gramáticas CFG a Forma Normal de Chomsky (CNF)
Implementa el algoritmo de simplificación y conversión a CNF
"""

class CNFConverter:
    def __init__(self, productions, terminals, non_terminals, start_symbol):
        self.productions = productions.copy()
        self.terminals = terminals.copy()
        self.non_terminals = non_terminals.copy()
        self.start_symbol = start_symbol
        self.new_var_counter = 0
        
    def convert(self):
        """Convierte la gramática a CNF"""
        print("\n🔄 Iniciando conversión a Forma Normal de Chomsky (CNF)...\n")
        
        # Paso 1: Eliminar producciones epsilon (si hay)
        self._eliminate_epsilon()
        
        # Paso 2: Eliminar producciones unitarias
        self._eliminate_unit_productions()
        
        # Paso 3: Convertir terminales en producciones mixtas
        self._replace_terminals()
        
        # Paso 4: Romper producciones largas
        self._break_long_productions()
        
        print("✅ Conversión a CNF completada\n")
        return self.productions, self.terminals, self.non_terminals, self.start_symbol
    
    def _eliminate_epsilon(self):
        """Elimina producciones epsilon (ε)"""
        # En esta gramática no hay producciones epsilon
        pass
    
    def _eliminate_unit_productions(self):
        """Elimina producciones unitarias (A -> B)"""
        print("📋 Paso 1: Eliminando producciones unitarias...")
        
        changed = True
        while changed:
            changed = False
            new_productions = {}
            
            for nt in self.productions:
                new_productions[nt] = []
                
                for prod in self.productions[nt]:
                    # Si es una producción unitaria (A -> B)
                    if len(prod) == 1 and prod[0] in self.non_terminals:
                        # Reemplazar con las producciones de B
                        target = prod[0]
                        if target in self.productions:
                            for target_prod in self.productions[target]:
                                if target_prod not in new_productions[nt]:
                                    new_productions[nt].append(target_prod)
                                    changed = True
                    else:
                        if prod not in new_productions[nt]:
                            new_productions[nt].append(prod)
            
            self.productions = new_productions
        
        print("   ✓ Producciones unitarias eliminadas")
    
    def _replace_terminals(self):
        """Reemplaza terminales en producciones mixtas"""
        print("📋 Paso 2: Reemplazando terminales en producciones mixtas...")
        
        terminal_vars = {}  # Mapeo de terminal -> nueva variable
        
        for nt in list(self.productions.keys()):
            new_prods = []
            
            for prod in self.productions[nt]:
                # Si la producción tiene más de un símbolo
                if len(prod) > 1:
                    new_prod = []
                    
                    for symbol in prod:
                        # Si es un terminal, crear nueva variable
                        if symbol in self.terminals:
                            if symbol not in terminal_vars:
                                new_var = self._new_variable()
                                terminal_vars[symbol] = new_var
                                self.non_terminals.add(new_var)
                                self.productions[new_var] = [[symbol]]
                            
                            new_prod.append(terminal_vars[symbol])
                        else:
                            new_prod.append(symbol)
                    
                    new_prods.append(new_prod)
                else:
                    new_prods.append(prod)
            
            self.productions[nt] = new_prods
        
        print("   ✓ Terminales reemplazados")
    
    def _break_long_productions(self):
        """Rompe producciones con más de 2 no-terminales"""
        print("📋 Paso 3: Rompiendo producciones largas...")
        
        changed = True
        while changed:
            changed = False
            new_productions = {}
            
            for nt in self.productions:
                new_productions[nt] = []
                
                for prod in self.productions[nt]:
                    # Si la producción tiene más de 2 símbolos
                    if len(prod) > 2:
                        # Crear nueva variable para los últimos símbolos
                        new_var = self._new_variable()
                        self.non_terminals.add(new_var)
                        
                        # A -> B C D E  se convierte en:
                        # A -> B X1
                        # X1 -> C X2
                        # X2 -> D E
                        new_productions[nt].append([prod[0], new_var])
                        new_productions[new_var] = [prod[1:]]
                        
                        changed = True
                    else:
                        new_productions[nt].append(prod)
            
            self.productions = new_productions
        
        print("   ✓ Producciones largas convertidas")
    
    def _new_variable(self):
        """Genera una nueva variable única"""
        while True:
            new_var = f"X{self.new_var_counter}"
            self.new_var_counter += 1
            if new_var not in self.non_terminals:
                return new_var
    
    def display_cnf(self):
        """Muestra la gramática en CNF"""
        print("=" * 60)
        print("GRAMÁTICA EN FORMA NORMAL DE CHOMSKY (CNF)")
        print("=" * 60)
        print(f"Símbolo inicial: {self.start_symbol}")
        print(f"\nNo-terminales: {sorted(self.non_terminals)}")
        print(f"\nTerminales: {sorted(self.terminals)}")
        print("\nProducciones en CNF:")
        
        for nt in sorted(self.productions.keys()):
            for prod in self.productions[nt]:
                prod_str = ' '.join(prod)
                # Verificar tipo de producción
                if len(prod) == 1 and prod[0] in self.terminals:
                    tipo = "(A -> a)"
                elif len(prod) == 2:
                    tipo = "(A -> BC)"
                else:
                    tipo = "(no CNF!)"
                
                print(f"  {nt} -> {prod_str} {tipo}")
        print("=" * 60)
