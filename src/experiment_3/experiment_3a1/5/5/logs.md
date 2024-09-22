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

\section*{Mathematical Model for Communication Network Optimization}

\subsection*{Sets}
\begin{itemize}
    \item Let \( N \) be the set of nodes, where \( N = \{1, 2, \ldots, n\} \).
    \item Let \( A \) be the set of links, where \( A = \{(i, j) \,|\, i, j \in N\} \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( U_{i,j} \): Maximum capacity of the link from node \( i \) to node \( j \) (in bits/second).
    \item \( C_{i,j} \): Cost per bit transmitted along the link from node \( i \) to node \( j \).
    \item \( B_{k,l} \): Data generation rate from node \( k \) to node \( l \) (in bits/second).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_{i,j} \): Flow of bits from node \( i \) to node \( j \) (in bits/second).
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{(i,j) \in A} C_{i,j} \cdot x_{i,j}
\]

\subsection*{Constraints}
1. Capacity constraints:
\[
0 \leq x_{i,j} \leq U_{i,j}, \quad \forall (i,j) \in A
\]

2. Flow conservation constraints for each node \( k \):
\[
\sum_{j \,:\, (k,j) \in A} x_{k,j} - \sum_{i \,:\, (i,k) \in A} x_{i,k} = 
\begin{cases}
B_{k,l}, & \text{if } k \text{ is source} \\
0, & \text{if } k \text{ is intermediate} \\
-B_{k,l}, & \text{if } k \text{ is sink}
\end{cases}, \quad \forall k \in N
\]

3. Non-negativity constraints:
\[
x_{i,j} \geq 0, \quad \forall (i,j) \in A
\]

\subsection*{Output}
The output will include the optimized paths, their flow, costs, and the total cost:
\begin{verbatim}
{
    "optimized_paths": {
        "paths": [
            {
                "source": k,
                "destination": l,
                "route": [k, i_1, i_2, ..., l],
                "path_flow": path_flow,
                "path_cost": path_cost
            },
            ...
        ],
    "total_cost": total_cost
}
\end{verbatim}

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

\section*{Mathematical Model for Communication Network Optimization}

\subsection*{Sets}
\begin{itemize}
    \item Let \( N \) be the set of nodes, where \( N = \{1, 2, \ldots, n\} \).
    \item Let \( A \) be the set of links, where \( A = \{(i, j) \,|\, i, j \in N\} \).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( U_{i,j} \): Maximum capacity of the link from node \( i \) to node \( j \) (in bits/second).
    \item \( C_{i,j} \): Cost per bit transmitted along the link from node \( i \) to node \( j \).
    \item \( B_{k,l} \): Data generation rate from node \( k \) to node \( l \) (in bits/second).
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_{i,j} \): Flow of bits from node \( i \) to node \( j \) (in bits/second).
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{(i,j) \in A} C_{i,j} \cdot x_{i,j}
\]

\subsection*{Constraints}
1. Capacity constraints:
\[
0 \leq x_{i,j} \leq U_{i,j}, \quad \forall (i,j) \in A
\]

2. Flow conservation constraints for each node \( k \):
\[
\sum_{j \,:\, (k,j) \in A} x_{k,j} - \sum_{i \,:\, (i,k) \in A} x_{i,k} = 
\begin{cases}
B_{k,l}, & \text{if } k \text{ is source} \\
0, & \text{if } k \text{ is intermediate} \\
-B_{k,l}, & \text{if } k \text{ is sink}
\end{cases}, \quad \forall k \in N
\]

3. Non-negativity constraints:
\[
x_{i,j} \geq 0, \quad \forall (i,j) \in A
\]

\subsection*{Output}
The output will include the optimized paths, their flow, costs, and the total cost:
\begin{verbatim}
{
    "optimized_paths": {
        "paths": [
            {
                "source": k,
                "destination": l,
                "route": [k, i_1, i_2, ..., l],
                "path_flow": path_flow,
                "path_cost": path_cost
            },
            ...
        ],
    "total_cost": total_cost
}
\end{verbatim}

\end{document}</MATH_MODEL>
<DATA>
{'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 'DataRate': [40, 30]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from the provided JSON
data = {'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 
        'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 'NumFlowReqs': 2, 
        'Source': [1, 2], 'Destination': [4, 3], 'DataRate': [40, 30]}

#### Define sets
N = range(1, max(data['StartNode'] + data['EndNode']) + 1)  #### Nodes
A = [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])]  #### Links

#### Parameters
U = {(data['StartNode'][i], data['EndNode'][i]): data['Capacity'][i] for i in range(data['NumLinks'])}
C = {(data['StartNode'][i], data['EndNode'][i]): data['Cost'][i] for i in range(data['NumLinks'])}
B = {(data['Source'][i], data['Destination'][i]): data['DataRate'][i] for i in range(data['NumFlowReqs'])}

#### Decision Variables
x = pulp.LpVariable.dicts('Flow', A, lowBound=0)

#### Problem Definition
problem = pulp.LpProblem("Communication_Network_Optimization", pulp.LpMinimize)

#### Objective Function
problem += pulp.lpSum(C[i, j] * x[i, j] for (i, j) in A)

#### Constraints
#### Capacity constraints
for (i, j) in A:
    problem += x[i, j] <= U[i, j]

#### Flow conservation constraints
for k in N:
    inflow = pulp.lpSum(x[i, k] for i in range(1, k+1) if (i, k) in A)  #### Incoming flow
    outflow = pulp.lpSum(x[k, j] for j in range(k+1, max(N)+1) if (k, j) in A)  #### Outgoing flow
    if k in data['Source']:
        problem += outflow - inflow == B[k, data['Destination'][data['Source'].index(k)]]
    elif k in data['Destination']:
        problem += inflow - outflow == B[data['Source'][data['Destination'].index(k)], k]
    else:
        problem += inflow == outflow

#### Solve the problem
problem.solve()

#### Preparing the output
optimized_paths = {
    "paths": [],
}
for (i, j) in A:
    if pulp.value(x[i, j]) > 0:
        path_flow = pulp.value(x[i, j])
        path_cost = path_flow * C[i, j]
        optimized_paths["paths"].append({
            "source": i,
            "destination": j,
            "route": [i, j],
            "path_flow": path_flow,
            "path_cost": path_cost
        })

total_cost = pulp.value(problem.objective)
optimized_paths["total_cost"] = total_cost

#### Print the objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
```

