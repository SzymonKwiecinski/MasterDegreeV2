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

\textbf{Sets:}
\begin{itemize}
    \item Let \( N \) be the set of nodes, where \( i, j, k, l \in N \).
    \item Let \( A \) be the set of ordered pairs representing communication links, where \( (i, j) \in A \).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( U_{i,j} \): Maximum capacity (bits/second) of link \( (i,j) \).
    \item \( C_{i,j} \): Cost per bit transmitted along link \( (i,j) \).
    \item \( B_{k,l} \): Data generation rate (bits/second) from source node \( k \) to destination node \( l \).
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( x_{i,j} \): Flow of data (bits/second) transmitted along link \( (i,j) \).
\end{itemize}

\textbf{Objective Function:}
Minimize the total cost:
\[
\text{Minimize} \quad Z = \sum_{(i,j) \in A} C_{i,j} \cdot x_{i,j}
\]

\textbf{Constraints:}
\begin{itemize}
    \item Capacity constraints:
    \[
    x_{i,j} \leq U_{i,j} \quad \forall (i,j) \in A
    \]
    
    \item Flow conservation for each node:
    \[
    \sum_{j: (i,j) \in A} x_{i,j} - \sum_{j: (j,i) \in A} x_{j,i} = 
    \begin{cases} 
    B_{k,l} & \text{if } i = k \\
    -B_{k,l} & \text{if } i = l \\
    0 & \text{otherwise}
    \end{cases} 
    \quad \forall i \in N
    \]
    
    \item Non-negativity constraints:
    \[
    x_{i,j} \geq 0 \quad \forall (i,j) \in A
    \]
\end{itemize}

\textbf{Output Specification:}
The output should include:
\begin{itemize}
    \item Optimized paths from each source \( k \) to its destination \( l \).
    \item The corresponding path flows and path costs.
    \item The total cost of all paths.
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

\textbf{Sets:}
\begin{itemize}
    \item Let \( N \) be the set of nodes, where \( i, j, k, l \in N \).
    \item Let \( A \) be the set of ordered pairs representing communication links, where \( (i, j) \in A \).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( U_{i,j} \): Maximum capacity (bits/second) of link \( (i,j) \).
    \item \( C_{i,j} \): Cost per bit transmitted along link \( (i,j) \).
    \item \( B_{k,l} \): Data generation rate (bits/second) from source node \( k \) to destination node \( l \).
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( x_{i,j} \): Flow of data (bits/second) transmitted along link \( (i,j) \).
\end{itemize}

\textbf{Objective Function:}
Minimize the total cost:
\[
\text{Minimize} \quad Z = \sum_{(i,j) \in A} C_{i,j} \cdot x_{i,j}
\]

\textbf{Constraints:}
\begin{itemize}
    \item Capacity constraints:
    \[
    x_{i,j} \leq U_{i,j} \quad \forall (i,j) \in A
    \]
    
    \item Flow conservation for each node:
    \[
    \sum_{j: (i,j) \in A} x_{i,j} - \sum_{j: (j,i) \in A} x_{j,i} = 
    \begin{cases} 
    B_{k,l} & \text{if } i = k \\
    -B_{k,l} & \text{if } i = l \\
    0 & \text{otherwise}
    \end{cases} 
    \quad \forall i \in N
    \]
    
    \item Non-negativity constraints:
    \[
    x_{i,j} \geq 0 \quad \forall (i,j) \in A
    \]
\end{itemize}

\textbf{Output Specification:}
The output should include:
\begin{itemize}
    \item Optimized paths from each source \( k \) to its destination \( l \).
    \item The corresponding path flows and path costs.
    \item The total cost of all paths.
\end{itemize}

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

#### Sets and Parameters
links = [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])]
capacity = {links[i]: data['Capacity'][i] for i in range(data['NumLinks'])}
cost = {links[i]: data['Cost'][i] for i in range(data['NumLinks'])}
flow_reqs = data['NumFlowReqs']
source_nodes = data['Source']
destination_nodes = data['Destination']
data_rates = data['DataRate']

#### Nodes set
nodes = set(data['StartNode'] + data['EndNode'])

#### Problem initialization
problem = pulp.LpProblem("Communication_Network", pulp.LpMinimize)

#### Decision Variables
flow = pulp.LpVariable.dicts("Flow", links, lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(cost[i, j] * flow[i, j] for i, j in links), "Total Cost"

#### Constraints
#### Capacity constraints
for i, j in links:
    problem += flow[i, j] <= capacity[i, j], f"Capacity_Constraint_{i}_{j}"
    
#### Flow conservation constraints
for node in nodes:
    for k in range(flow_reqs):
        if node == source_nodes[k]:
            net_flow = data_rates[k]
        elif node == destination_nodes[k]:
            net_flow = -data_rates[k]
        else:
            net_flow = 0
           
        problem += (
            pulp.lpSum(flow[i, j] for i, j in links if i == node) -
            pulp.lpSum(flow[j, i] for j, i in links if i == node) == net_flow,
            f"Flow_Conservation_Node_{node}_Req_{k}"
        )

#### Solve the problem
problem.solve()

#### Print the outputs
print("Optimized path flows and costs:")
for i, j in links:
    print(f"Flow on link ({i} -> {j}): {flow[i, j].varValue} bits/second with cost: {cost[i, j] * flow[i, j].varValue}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


