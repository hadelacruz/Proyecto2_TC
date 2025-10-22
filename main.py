from grammar_parser import GrammarParser
from cnf_converter import CNFConverter
from cyk_algorithm import CYKAlgorithm

def print_header():
    print("\n" + "=" * 80)
    print(" " * 20 + "ALGORITMO CYK - ANÁLISIS SINTÁCTICO")
    print(" " * 15 + "Forma Normal de Chomsky (CNF)")
    print(" " * 18 + "Programación Dinámica")
    print("=" * 80)

def print_result(belongs, elapsed_time):
    print("\n" + "=" * 80)
    print("RESULTADO DEL ANÁLISIS")
    print("=" * 80)
    
    if belongs:
        print("Respuesta: SÍ")
        print("   La frase PERTENECE al lenguaje generado por la gramática")
    else:
        print("Respuesta: NO")
        print("   La frase NO PERTENECE al lenguaje generado por la gramática")
    
    print(f"\nTiempo de ejecución: {elapsed_time:.6f} segundos")
    print("=" * 80)

def main():
    print_header()
    
    # Paso 1: Leer y parsear la gramática
    print("\nPaso 1: Leyendo gramática desde archivo...")
    grammar_file = "grammar.txt"
    
    try:
        parser = GrammarParser(grammar_file)
        productions, terminals, non_terminals, start_symbol = parser.parse()
        parser.display_grammar()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{grammar_file}'")
        return
    except Exception as e:
        print(f"Error al parsear la gramática: {e}")
        return
    
    # Paso 2: Convertir a CNF
    print("\nPaso 2: Convirtiendo gramática a Forma Normal de Chomsky...")
    converter = CNFConverter(productions, terminals, non_terminals, start_symbol)
    cnf_productions, cnf_terminals, cnf_non_terminals, cnf_start = converter.convert()
    converter.display_cnf()
    
    # Paso 3: Interfaz de usuario para analizar frases
    print("\n" + "=" * 80)
    print("ANÁLISIS DE FRASES")
    print("=" * 80)
    print("Ingrese frases en inglés para analizar si pertenecen al lenguaje.")
    print("Escriba 'salir' o 'exit' para terminar.\n")
    
    cyk = CYKAlgorithm(cnf_productions, cnf_terminals, cnf_non_terminals, cnf_start)
    
    while True:
        sentence = input("Ingrese una frase: ").strip()
        
        if sentence.lower() in ['salir', 'exit', 'quit', 'q']:
            print("\n¡Hasta luego!")
            break
        
        if not sentence:
            print("Por favor ingrese una frase válida.\n")
            continue
        
        # Aplicar algoritmo CYK
        belongs, elapsed_time, words = cyk.parse(sentence)
        
        # Mostrar tabla de programación dinámica
        cyk.display_table(words)
        
        # Mostrar resultado
        print_result(belongs, elapsed_time)
        
        # Si pertenece, construir y mostrar el árbol de análisis
        if belongs:
            tree = cyk.build_parse_tree_fixed(words)
            
            if tree:
                print("ÁRBOL DE ANÁLISIS SINTÁCTICO")
                print("=" * 80)
                print()
                # Convertir a NLTK Tree y mostrar en formato ASCII
                nltk_tree = cyk.build_nltk_tree(tree)
                if nltk_tree:
                    nltk_tree.pretty_print(unicodelines=True, nodedist=2)
                print("=" * 80)
            else:
                print("No se pudo construir el árbol de análisis.")
        
if __name__ == "__main__":
    main()
