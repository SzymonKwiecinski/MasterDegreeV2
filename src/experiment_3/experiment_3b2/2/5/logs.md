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

\section*{Linear Programming Model for Network Flow Optimization}

Consider a communication network defined by a set of nodes and links. We aim to optimize the flow of data while minimizing costs. Below is the formulation of the problem as a linear programming model.

\subsection*{Sets and Indices}
\begin{itemize}
    \item \( N \): Set of nodes
    \item \( A \): Set of directed links \((i, j)\)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( U_{i,j} \): Capacity of link \((i, j) \in A\) in bits per second
    \item \( C_{i,j} \): Cost per bit on link \((i, j) \in A\)
    \item \( B_{k,l} \): Data rate from node \( k \) to node \( l \) in bits per second
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( f_{i,j}^{k,l} \): Flow from node \( k \) to node \( l \) on link \((i, j)\)
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost of data transmission:
\[
\text{Minimize} \quad Z = \sum_{(i,j) \in A} \sum_{(k,l) \in N \times N} C_{i,j} \cdot f_{i,j}^{k,l}
\]

\subsection*{Constraints}
\begin{align*}
\text{Capacity Constraints:} \quad & \sum_{(k,l) \in N \times N} f_{i,j}^{k,l} \leq U_{i,j}, \quad \forall (i,j) \in A \\
\text{Flow Conservation:} \quad & \sum_{j : (i,j) \in A} f_{i,j}^{k,l} - \sum_{j : (j,i) \in A} f_{j,i}^{k,l} = 
\begin{cases} 
B_{k,l}, & \text{if } i = k \\ 
-B_{k,l}, & \text{if } i = l \\ 
0, & \text{otherwise} 
\end{cases} \quad \forall i \in N, \forall (k,l) \in N \times N
\end{align*}

The above model will yield the optimal flow distribution that minimizes the total transmission cost while ensuring data reaches from sources to destinations under given constraints.

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

\section*{Linear Programming Model for Network Flow Optimization}

Consider a communication network defined by a set of nodes and links. We aim to optimize the flow of data while minimizing costs. Below is the formulation of the problem as a linear programming model.

\subsection*{Sets and Indices}
\begin{itemize}
    \item \( N \): Set of nodes
    \item \( A \): Set of directed links \((i, j)\)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( U_{i,j} \): Capacity of link \((i, j) \in A\) in bits per second
    \item \( C_{i,j} \): Cost per bit on link \((i, j) \in A\)
    \item \( B_{k,l} \): Data rate from node \( k \) to node \( l \) in bits per second
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( f_{i,j}^{k,l} \): Flow from node \( k \) to node \( l \) on link \((i, j)\)
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost of data transmission:
\[
\text{Minimize} \quad Z = \sum_{(i,j) \in A} \sum_{(k,l) \in N \times N} C_{i,j} \cdot f_{i,j}^{k,l}
\]

\subsection*{Constraints}
\begin{align*}
\text{Capacity Constraints:} \quad & \sum_{(k,l) \in N \times N} f_{i,j}^{k,l} \leq U_{i,j}, \quad \forall (i,j) \in A \\
\text{Flow Conservation:} \quad & \sum_{j : (i,j) \in A} f_{i,j}^{k,l} - \sum_{j : (j,i) \in A} f_{j,i}^{k,l} = 
\begin{cases} 
B_{k,l}, & \text{if } i = k \\ 
-B_{k,l}, & \text{if } i = l \\ 
0, & \text{otherwise} 
\end{cases} \quad \forall i \in N, \forall (k,l) \in N \times N
\end{align*}

The above model will yield the optimal flow distribution that minimizes the total transmission cost while ensuring data reaches from sources to destinations under given constraints.

\end{document}</MATH_MODEL>
<DATA>
{'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 'DataRate': [40, 30]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
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

#### Sets and indices
N = set(data['Source'] + data['Destination'])
A = [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])]

#### Parameters
U = {(data['StartNode'][i], data['EndNode'][i]): data['Capacity'][i] for i in range(data['NumLinks'])}
C = {(data['StartNode'][i], data['EndNode'][i]): data['Cost'][i] for i in range(data['NumLinks'])}
B = {(data['Source'][k], data['Destination'][k]): data['DataRate'][k] for k in range(data['NumFlowReqs'])}

#### Decision Variables
f = pulp.LpVariable.dicts("flow", [(i, j, k, l) for (i, j) in A for (k, l) in B.keys()], lowBound=0)

#### Problem Definition
problem = pulp.LpProblem("Network_Flow_Optimization", pulp.LpMinimize)

#### Objective Function
problem += pulp.lpSum(C[i, j] * f[i, j, k, l] for (i, j) in A for (k, l) in B.keys()), "Total_Cost"

#### Capacity Constraints
for (i, j) in A:
    problem += (pulp.lpSum(f[i, j, k, l] for (k, l) in B.keys()) <= U[i, j]), f"Capacity_Constraint_{i}_{j}"

#### Flow Conservation Constraints
for i in N:
    for (k, l) in B.keys():
        inflow = pulp.lpSum(f[j, i, k, l] for (j, i) in A if (j, i) in A)
        outflow = pulp.lpSum(f[i, j, k, l] for (i, j) in A if (i, j) in A)
        
        if i == k:
            problem += (outflow - inflow == B[k, l]), f"Flow_Conservation_Entry_{i}_{k}_{l}"
        elif i == l:
            problem += (inflow - outflow == B[k, l]), f"Flow_Conservation_Exit_{i}_{k}_{l}"
        else:
            problem += (inflow - outflow == 0), f"Flow_Conservation_Intermediate_{i}_{k}_{l}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

