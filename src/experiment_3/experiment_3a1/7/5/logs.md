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

\section*{Linear Programming Model for Communication Network}

\textbf{Indices:}
\begin{itemize}
    \item \(i, j\): Nodes in the communication network.
    \item \(k, l\): Source and destination nodes, respectively.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \(A\): Set of all links.
    \item \(U_{i,j}\): Maximum bits per second that link \((i, j)\) can carry.
    \item \(C_{i,j}\): Cost per bit transmitted along link \((i, j)\).
    \item \(B_{k,l}\): Data generation rate from node \(k\) to node \(l\).
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \(x_{i,j}\): Flow of data along link \((i,j)\).
\end{itemize}

\textbf{Objective Function:}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{(i,j) \in A} C_{i,j} \cdot x_{i,j}
\]

\textbf{Subject to:}
\begin{itemize}
    \item Capacity constraints:
    \[
    x_{i,j} \leq U_{i,j} \quad \forall (i,j) \in A
    \]
    
    \item Flow conservation constraints for each node \(k\):
    \[
    \sum_{j: (k,j) \in A} x_{k,j} - \sum_{i: (i,k) \in A} x_{i,k} = 
    \begin{cases}
        B_{k,l} & \text{if } k = k \text{ and } l \text{ is the destination} \\
        0 & \text{otherwise}
    \end{cases}
    \]
    for all nodes \(k\).
    
    \item Non-negativity constraints:
    \[
    x_{i,j} \geq 0 \quad \forall (i,j) \in A
    \]
\end{itemize}

\textbf{Output:}
\begin{itemize}
    \item \textbf{optimized paths:}
        \begin{itemize}
            \item \texttt{paths}: List of paths from source to destination, including route and corresponding flows and costs.
            \item \texttt{total\_cost}: Total cost of all paths.
        \end{itemize}
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

\section*{Linear Programming Model for Communication Network}

\textbf{Indices:}
\begin{itemize}
    \item \(i, j\): Nodes in the communication network.
    \item \(k, l\): Source and destination nodes, respectively.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \(A\): Set of all links.
    \item \(U_{i,j}\): Maximum bits per second that link \((i, j)\) can carry.
    \item \(C_{i,j}\): Cost per bit transmitted along link \((i, j)\).
    \item \(B_{k,l}\): Data generation rate from node \(k\) to node \(l\).
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \(x_{i,j}\): Flow of data along link \((i,j)\).
\end{itemize}

\textbf{Objective Function:}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{(i,j) \in A} C_{i,j} \cdot x_{i,j}
\]

\textbf{Subject to:}
\begin{itemize}
    \item Capacity constraints:
    \[
    x_{i,j} \leq U_{i,j} \quad \forall (i,j) \in A
    \]
    
    \item Flow conservation constraints for each node \(k\):
    \[
    \sum_{j: (k,j) \in A} x_{k,j} - \sum_{i: (i,k) \in A} x_{i,k} = 
    \begin{cases}
        B_{k,l} & \text{if } k = k \text{ and } l \text{ is the destination} \\
        0 & \text{otherwise}
    \end{cases}
    \]
    for all nodes \(k\).
    
    \item Non-negativity constraints:
    \[
    x_{i,j} \geq 0 \quad \forall (i,j) \in A
    \]
\end{itemize}

\textbf{Output:}
\begin{itemize}
    \item \textbf{optimized paths:}
        \begin{itemize}
            \item \texttt{paths}: List of paths from source to destination, including route and corresponding flows and costs.
            \item \texttt{total\_cost}: Total cost of all paths.
        \end{itemize}
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 'DataRate': [40, 30]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

data = {'NumLinks': 4, 
        'StartNode': [1, 2, 2, 3], 
        'EndNode': [2, 3, 4, 4], 
        'Capacity': [50, 40, 60, 50], 
        'Cost': [2, 3, 1, 1], 
        'NumFlowReqs': 2, 
        'Source': [1, 2], 
        'Destination': [4, 3], 
        'DataRate': [40, 30]}

#### Extract data
A = [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])]
U = {(data['StartNode'][i], data['EndNode'][i]): data['Capacity'][i] for i in range(data['NumLinks'])}
C = {(data['StartNode'][i], data['EndNode'][i]): data['Cost'][i] for i in range(data['NumLinks'])}
B = {(data['Source'][k], data['Destination'][k]): data['DataRate'][k] for k in range(data['NumFlowReqs'])}

#### Initialize the problem
problem = pulp.LpProblem("Communication_Network", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("flow", A, lowBound=0)

#### Objective function
problem += pulp.lpSum(C[i, j] * x[i, j] for (i, j) in A), "Total_Cost"

#### Capacity constraints
for (i, j) in A:
    problem += x[i, j] <= U[i, j], f"Capacity_Constraint_{i}_{j}"

#### Flow conservation constraints
for k in data['Source']:
    for l in data['Destination']:
        if (k, l) in B:
            #### Incoming flow
            problem += (pulp.lpSum(x[i, j] for (i, j) in A if j == l) - 
                         pulp.lpSum(x[i, j] for (i, j) in A if i == k)) == B[k, l], f"Flow_Conservation_{k}_{l}"
                        )
        else:
            #### No data flow
            problem += (pulp.lpSum(x[i, j] for (i, j) in A if j == k) - 
                         pulp.lpSum(x[i, j] for (i, j) in A if i == k)) == 0, f"No_Flow_Conservation_{k}"
                        )

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

