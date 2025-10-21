# Proyecto 2 - Teoría de Computación
## Algoritmo CYK con Conversión a CNF

### 📋 Descripción
Este proyecto implementa el **algoritmo CYK (Cocke-Younger-Kasami)** para determinar si una frase en inglés pertenece a un lenguaje generado por una gramática libre de contexto (CFG). El algoritmo utiliza **programación dinámica** y requiere que la gramática esté en **Forma Normal de Chomsky (CNF)**.

### 🎯 Objetivos
- ✅ Implementación del algoritmo de simplificación de gramáticas (conversión a CNF)
- ✅ Implementación del algoritmo CYK con programación dinámica
- ✅ Construcción del árbol de análisis sintáctico (parse tree)

### 🗂️ Estructura del Proyecto
```
Proyecto2_TC/
│
├── grammar.txt          # Archivo con la gramática CFG
├── grammar_parser.py    # Parser de gramáticas CFG
├── cnf_converter.py     # Conversor a Forma Normal de Chomsky
├── cyk_algorithm.py     # Implementación del algoritmo CYK
├── main.py              # Programa principal
└── README.md            # Este archivo
```

### 📝 Gramática Utilizada
```
S → NP VP
VP → VP PP | V NP | cooks | drinks | eats | cuts
PP → P NP
NP → Det N | he | she
V → cooks | drinks | eats | cuts
P → in | with
N → cat | dog | beer | cake | juice | meat | soup | fork | knife | oven | spoon
Det → a | the
```

### 🚀 Uso

#### Requisitos
- Python 3.6 o superior
- No requiere bibliotecas externas

#### Ejecución
```bash
python main.py
```

### 💡 Ejemplos

#### ✅ Frases que PERTENECEN al lenguaje:
1. `she eats a cake`
2. `he drinks the beer`
3. `she cooks the soup`
4. `he cuts the meat with a knife`
5. `she eats a cake with a fork`
6. `the cat drinks the beer`
7. `the dog eats the meat`

#### ❌ Frases que NO PERTENECEN al lenguaje:
1. `she drinks` (falta objeto)
2. `eats a cake` (falta sujeto)
3. `she quickly eats cake` ("quickly" no está en gramática)
4. `the dog cat eats` (estructura incorrecta)
5. `she eat a cake` ("eat" no está en gramática, solo "eats")
6. `a fork cuts the meat` ("fork" no puede ser sujeto)

### 🔄 Proceso del Algoritmo

#### 1️⃣ Parsing de Gramática
- Lee el archivo `grammar.txt`
- Identifica terminales y no-terminales
- Construye la estructura de producciones

#### 2️⃣ Conversión a CNF
La conversión incluye:
- **Eliminación de producciones unitarias** (A → B)
- **Reemplazo de terminales** en producciones mixtas
- **Ruptura de producciones largas** (A → BCD se convierte en A → BX, X → CD)

Formas permitidas en CNF:
- `A → BC` (dos no-terminales)
- `A → a` (un terminal)

#### 3️⃣ Algoritmo CYK
- **Entrada**: Frase tokenizada
- **Proceso**: Llena tabla de programación dinámica
  - Diagonal: subcadenas de longitud 1
  - Niveles superiores: subcadenas más largas
- **Salida**: SÍ/NO según si S ∈ T[0][n]

#### 4️⃣ Construcción del Parse Tree
Si la frase pertenece al lenguaje, se reconstruye el árbol de análisis usando información almacenada durante el algoritmo CYK.

### 📊 Salida del Programa

El programa muestra:
1. **Gramática original (CFG)**
2. **Gramática en CNF** con anotaciones
3. **Tabla de programación dinámica** (CYK)
4. **Resultado**: SÍ o NO
5. **Tiempo de ejecución**
6. **Árbol de análisis sintáctico** (si aplica)

