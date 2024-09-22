# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- An Italian transport company must send empty containers from its depots to ports. 
- The number of containers available in the depot \var{i} is denoted with \var{numdepot_i}. 
- Container requirement in port \var{j} is \var{numport_{j}}. 
- Transport of containers is by barges. 
- Each barge can only contain two containers and the cost of transport (per barge) is proportional to the distance traveled (price is \var{price} Euros/km).
- The distances between depot \var{i} and port \var{j} is \var{distance_{i, j}}.

INPUT FORMAT:

{
	"numdepot": [numdepot_{i} for i in 1,...,I],
	"numport": [numport_{j} for j in 1,...,J],
	"price": price,
	"distance": [[distance_{i, j} for i in 1,...I] for j in 1,...,J]
}


OBJECTIVE: Minimize the total transportation cost.

OUTPUT INFO:

\var{number} represents the number of containers sent from each depot to port

OUTPUT FORMAT:

{
	"number": [[number_{i, j} for i in 1,...,I] for j in 1,...,J]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Sets}
\begin{itemize}
    \item $I$: Set of depots, indexed by $i$.
    \item $J$: Set of ports, indexed by $j$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $numdepot_i$: Number of containers available in depot $i$.
    \item $numport_j$: Container requirement in port $j$.
    \item $price$: Cost of transport per kilometer.
    \item $distance_{i,j}$: Distance between depot $i$ and port $j$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $number_{i,j}$: Number of containers sent from depot $i$ to port $j$.
\end{itemize}

\subsection*{Objective Function}
\[
\text{Minimize } Z = \sum_{i=1}^{I} \sum_{j=1}^{J} \left( \frac{number_{i,j}}{2} \cdot distance_{i,j} \cdot price \right)
\]

\subsection*{Constraints}
\begin{align}
\sum_{j=1}^{J} number_{i,j} & \leq numdepot_i, \quad \forall i \in \{1, \ldots, I\} \quad \text{(Depot capacity constraints)} \\
\sum_{i=1}^{I} number_{i,j} & \geq numport_j, \quad \forall j \in \{1, \ldots, J\} \quad \text{(Port demand constraints)} \\
number_{i,j} & \geq 0, \quad \forall i \in \{1, \ldots, I\}, j \in \{1, \ldots, J\} \quad \text{(Non-negativity constraints)}
\end{align}

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Sets}
\begin{itemize}
    \item $I$: Set of depots, indexed by $i$.
    \item $J$: Set of ports, indexed by $j$.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $numdepot_i$: Number of containers available in depot $i$.
    \item $numport_j$: Container requirement in port $j$.
    \item $price$: Cost of transport per kilometer.
    \item $distance_{i,j}$: Distance between depot $i$ and port $j$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $number_{i,j}$: Number of containers sent from depot $i$ to port $j$.
\end{itemize}

\subsection*{Objective Function}
\[
\text{Minimize } Z = \sum_{i=1}^{I} \sum_{j=1}^{J} \left( \frac{number_{i,j}}{2} \cdot distance_{i,j} \cdot price \right)
\]

\subsection*{Constraints}
\begin{align}
\sum_{j=1}^{J} number_{i,j} & \leq numdepot_i, \quad \forall i \in \{1, \ldots, I\} \quad \text{(Depot capacity constraints)} \\
\sum_{i=1}^{I} number_{i,j} & \geq numport_j, \quad \forall j \in \{1, \ldots, J\} \quad \text{(Port demand constraints)} \\
number_{i,j} & \geq 0, \quad \forall i \in \{1, \ldots, I\}, j \in \{1, \ldots, J\} \quad \text{(Non-negativity constraints)}
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data from the given JSON format
data_json = '''{'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}'''
data = json.loads(data_json.replace("'", "\""))

#### Sets
I = range(len(data['numdepot']))
J = range(len(data['numport']))

#### Parameters
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

#### Decision Variables
number = pulp.LpVariable.dicts("number", (I, J), lowBound=0, cat='Continuous')

#### Problem Definition
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

#### Objective Function
problem += pulp.lpSum((number[i][j] / 2) * distance[i][j] * price for i in I for j in J)

#### Constraints
#### Depot capacity constraints
for i in I:
    problem += pulp.lpSum(number[i][j] for j in J) <= numdepot[i]

#### Port demand constraints
for j in J:
    problem += pulp.lpSum(number[i][j] for i in I) >= numport[j]

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

