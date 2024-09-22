# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- Consider a communication network consisting of \var{n} nodes.
- Nodes are con­nected by communication links.
- A link allowing one-way transmission from node \var{i} to node \var{j} is described by an ordered pair (\var{i},\var{j}). 
- Let \var{A} be the set of all links. 
- We assume that each link (\var{i},\var{j}) \in \var{A} can carry up to \var{U_{i,j}} bits per second. 
- There is a positive cost \var{C_{i,j}} per bit transmitted along that link. 
- Each node \var{k} generates data, at the rate of \var{B_{k,l}} bits per second, that have to be transmitted to node \var{l}, either through a direct link (\var{k}, \var{l}) or by tracing a sequence of links. 
- We allow the data with the same origin and destination to be split and be transmitted along different paths.

INPUT FORMAT:

{
    "links": [
       {
        "start": i,
        "end": j,
        "U": U_{i,j},
        "C": C_{i,j},
       }
    ],
    "data": [
        {
            "source": k,
            "destination": l,
            "rate": B_{k,l}
        }
    ]
}


OBJECTIVE: Find paths along which all data reach their intended destinations, while minimizing the total cost. 



OUTPUT INFO:
- \var{total_cost} represents the total cost of all the paths
- \var{path_cost} represents the cost of the corresponding path
- \var{path_flow} represents the flow going through the corresponding path

OUTPUT FORMAT:

{
    "optimized_paths": {
        "paths": [
            {
                "source": k,
                "destination": l,
                "route": [k, i_1, i_2, ..., l],
                "path_flow": path_flow
                "path_cost": path_cost
            },
            for id in 1, ..., m 
        ],
    "total_cost": "total_cost"
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Communication Network Optimization}

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( x_{i,j} \): the flow of data from node \( i \) to node \( j \).
\end{itemize}

\subsection*{Parameters}
Given:
\begin{itemize}
    \item \( A \): the set of all links in the network.
    \item \( U_{i,j} \): the maximum capacity (bits per second) of link \( (i,j) \).
    \item \( C_{i,j} \): the cost (per bit) of transmitting data along link \( (i,j) \).
    \item \( B_{k,l} \): the data generation rate (bits per second) from node \( k \) to node \( l \).
    \item \( K \): the set of all source nodes.
    \item \( L \): the set of all destination nodes.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{(i,j) \in A} C_{i,j} \cdot x_{i,j}
\]

\subsection*{Constraints}
1. Flow conservation at each node \( k \) (except for source and destination):
\[
\sum_{j: (k,j) \in A} x_{k,j} - \sum_{i: (i,k) \in A} x_{i,k} = 0 \quad \forall k \in (K \cup L), k \text{ not a source or destination}
\]

2. Supply at source nodes:
\[
\sum_{j: (k,j) \in A} x_{k,j} = B_{k,l} \quad \forall k \in K
\]

3. Demand at destination nodes:
\[
\sum_{i: (i,l) \in A} x_{i,l} = B_{k,l} \quad \forall l \in L
\]

4. Capacity constraints:
\[
0 \leq x_{i,j} \leq U_{i,j} \quad \forall (i,j) \in A
\]

\subsection*{Output}
The solution will provide:
\begin{itemize}
    \item \texttt{optimized\_paths}: a list of paths and their corresponding flow and cost.
    \item \texttt{total\_cost}: total cost of all paths.
\end{itemize}

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

\section*{Linear Programming Model for Communication Network Optimization}

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( x_{i,j} \): the flow of data from node \( i \) to node \( j \).
\end{itemize}

\subsection*{Parameters}
Given:
\begin{itemize}
    \item \( A \): the set of all links in the network.
    \item \( U_{i,j} \): the maximum capacity (bits per second) of link \( (i,j) \).
    \item \( C_{i,j} \): the cost (per bit) of transmitting data along link \( (i,j) \).
    \item \( B_{k,l} \): the data generation rate (bits per second) from node \( k \) to node \( l \).
    \item \( K \): the set of all source nodes.
    \item \( L \): the set of all destination nodes.
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{(i,j) \in A} C_{i,j} \cdot x_{i,j}
\]

\subsection*{Constraints}
1. Flow conservation at each node \( k \) (except for source and destination):
\[
\sum_{j: (k,j) \in A} x_{k,j} - \sum_{i: (i,k) \in A} x_{i,k} = 0 \quad \forall k \in (K \cup L), k \text{ not a source or destination}
\]

2. Supply at source nodes:
\[
\sum_{j: (k,j) \in A} x_{k,j} = B_{k,l} \quad \forall k \in K
\]

3. Demand at destination nodes:
\[
\sum_{i: (i,l) \in A} x_{i,l} = B_{k,l} \quad \forall l \in L
\]

4. Capacity constraints:
\[
0 \leq x_{i,j} \leq U_{i,j} \quad \forall (i,j) \in A
\]

\subsection*{Output}
The solution will provide:
\begin{itemize}
    \item \texttt{optimized\_paths}: a list of paths and their corresponding flow and cost.
    \item \texttt{total\_cost}: total cost of all paths.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 'DataRate': [40, 30]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extract data from the JSON format
data = {
    'NumLinks': 4, 
    'StartNode': [1, 2, 2, 3], 
    'EndNode': [2, 3, 4, 4], 
    'Capacity': [50, 40, 60, 50], 
    'Cost': [2, 3, 1, 1], 
    'NumFlowReqs': 2, 
    'Source': [1, 2], 
    'Destination': [4, 3], 
    'DataRate': [40, 30]
}

#### Define sets and parameters
A = list(zip(data['StartNode'], data['EndNode']))
U = {(i, j): data['Capacity'][index] for index, (i, j) in enumerate(A)}
C = {(i, j): data['Cost'][index] for index, (i, j) in enumerate(A)}
K = data['Source']
L = data['Destination']
B = {(k, l): data['DataRate'][index] for index, (k, l) in enumerate(zip(K, L))}

#### Initialize the LP problem
problem = pulp.LpProblem("Communication_Network_Optimization", pulp.LpMinimize)

#### Define variables
x = pulp.LpVariable.dicts("Flow", A, lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(C[i, j] * x[i, j] for (i, j) in A), "Total Cost"

#### Flow conservation constraints
all_nodes = set(data['StartNode']) | set(data['EndNode'])

for k in all_nodes:
    if k not in K and k not in L:
        problem += (pulp.lpSum(x[k, j] for (k, j) in A if k == k) -
                    pulp.lpSum(x[i, k] for (i, k) in A if k == k) == 0), f"Flow_Conservation_at_{k}"

#### Supply constraints at source nodes
for k in K:
    l = L[K.index(k)]
    problem += (pulp.lpSum(x[k, j] for (k, j) in A if k == k) == B[k, l]), f"Supply_at_Source_{k}"

#### Demand constraints at destination nodes
for l in L:
    k = K[L.index(l)]
    problem += (pulp.lpSum(x[i, l] for (i, l) in A if l == l) == B[k, l]), f"Demand_at_Destination_{l}"

#### Capacity constraints
for i, j in A:
    problem += (x[i, j] <= U[i, j]), f"Capacity_{i}_{j}"

#### Solve the problem
problem.solve()

#### Print the results
optimized_paths = [(i, j, pulp.value(x[i, j]), C[i, j] * pulp.value(x[i, j])) for (i, j) in A if pulp.value(x[i, j]) > 0]
total_cost = pulp.value(problem.objective)

print(f"Optimized Paths and Flow:")
for path in optimized_paths:
    print(f"From Node {path[0]} to Node {path[1]}: Flow={path[2]} with Cost={path[3]}")
print(f"Total Cost: {total_cost}")

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

