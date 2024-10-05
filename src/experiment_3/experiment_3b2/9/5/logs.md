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
To model this communication network problem as a Linear Programming (LP) problem, we will define the variables, objective function, and constraints using the given problem description. We aim to minimize the total cost of data transmission across the network, considering the constraints on link capacities and the requirement that each node's generated data reaches its destination.

Here is the LP formulation in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Sets and Indices:}
\begin{itemize}
    \item Nodes: $N = \{1, 2, \ldots, n\}$
    \item Links: $A = \{(i, j) \mid i, j \in N\}$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $U_{i,j}$: Maximum capacity (bits per second) for link $(i,j) \in A$
    \item $C_{i,j}$: Cost per bit for link $(i,j) \in A$
    \item $B_{k,l}$: Data rate (bits per second) from node $k$ to node $l$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $f_{i,j}^{k,l}$: Flow (bits per second) on link $(i,j) \in A$ for data from source $k$ to destination $l$
\end{itemize}

\textbf{Objective Function:}
Minimize the total transmission cost:
\[
\text{Minimize } Z = \sum_{(i,j) \in A} \sum_{(k,l)} C_{i,j} \cdot f_{i,j}^{k,l}
\]

\textbf{Constraints:}
\begin{itemize}
    \item \textbf{Flow Conservation:} For each $(k,l)$ and each node $i \neq k,l$:
    \[
    \sum_{j: (i,j) \in A} f_{i,j}^{k,l} - \sum_{j: (j,i) \in A} f_{j,i}^{k,l} = 
    \begin{cases} 
    B_{k,l}, & \text{if } i = k \\
    -B_{k,l}, & \text{if } i = l \\
    0, & \text{otherwise}
    \end{cases}
    \]

    \item \textbf{Capacity Constraints:} For each link $(i,j) \in A$:
    \[
    \sum_{k,l} f_{i,j}^{k,l} \leq U_{i,j}
    \]

    \item \textbf{Non-negativity Constraints:} 
    \[
    f_{i,j}^{k,l} \geq 0 \quad \forall (i,j) \in A, \forall (k,l)
    \]
\end{itemize}

\end{document}
```

This LP formulation aims to minimize the total cost of transmitting data through the network while respecting the link capacities and ensuring that the data generated at each node reaches its intended destination. The decision variables \( f_{i,j}^{k,l} \) represent the flow of data from source \( k \) to destination \( l \) across the link \( (i,j) \). The constraints ensure flow conservation at each node and do not exceed link capacities.

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

\textbf{Sets and Indices:}
\begin{itemize}
    \item Nodes: $N = \{1, 2, \ldots, n\}$
    \item Links: $A = \{(i, j) \mid i, j \in N\}$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $U_{i,j}$: Maximum capacity (bits per second) for link $(i,j) \in A$
    \item $C_{i,j}$: Cost per bit for link $(i,j) \in A$
    \item $B_{k,l}$: Data rate (bits per second) from node $k$ to node $l$
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $f_{i,j}^{k,l}$: Flow (bits per second) on link $(i,j) \in A$ for data from source $k$ to destination $l$
\end{itemize}

\textbf{Objective Function:}
Minimize the total transmission cost:
\[
\text{Minimize } Z = \sum_{(i,j) \in A} \sum_{(k,l)} C_{i,j} \cdot f_{i,j}^{k,l}
\]

\textbf{Constraints:}
\begin{itemize}
    \item \textbf{Flow Conservation:} For each $(k,l)$ and each node $i \neq k,l$:
    \[
    \sum_{j: (i,j) \in A} f_{i,j}^{k,l} - \sum_{j: (j,i) \in A} f_{j,i}^{k,l} = 
    \begin{cases} 
    B_{k,l}, & \text{if } i = k \\
    -B_{k,l}, & \text{if } i = l \\
    0, & \text{otherwise}
    \end{cases}
    \]

    \item \textbf{Capacity Constraints:} For each link $(i,j) \in A$:
    \[
    \sum_{k,l} f_{i,j}^{k,l} \leq U_{i,j}
    \]

    \item \textbf{Non-negativity Constraints:} 
    \[
    f_{i,j}^{k,l} \geq 0 \quad \forall (i,j) \in A, \forall (k,l)
    \]
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 'DataRate': [40, 30]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
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

#### Extract data
num_links = data['NumLinks']
start_nodes = data['StartNode']
end_nodes = data['EndNode']
capacities = data['Capacity']
costs = data['Cost']
num_flow_reqs = data['NumFlowReqs']
sources = data['Source']
destinations = data['Destination']
data_rates = data['DataRate']

#### Create a linear programming problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

#### Decision variables
flow_vars = {}
for k in range(num_flow_reqs):
    for i in range(num_links):
        flow_vars[(k, i)] = pulp.LpVariable(f'f_{sources[k]}_{start_nodes[i]}_{end_nodes[i]}_{destinations[k]}', lowBound=0)

#### Objective function
problem += pulp.lpSum(costs[i] * flow_vars[(k, i)] for k in range(num_flow_reqs) for i in range(num_links)), "Total_Cost"

#### Flow Conservation Constraints
for k in range(num_flow_reqs):
    for node in set(start_nodes + end_nodes):
        if node == sources[k]:
            problem += (pulp.lpSum(flow_vars[(k, i)] for i in range(num_links) if start_nodes[i] == node) -
                         pulp.lpSum(flow_vars[(k, i)] for i in range(num_links) if end_nodes[i] == node) == data_rates[k], 
                         f"Flow_Conservation_Source_{k}_Node_{node}")
        elif node == destinations[k]:
            problem += (pulp.lpSum(flow_vars[(k, i)] for i in range(num_links) if start_nodes[i] == node) -
                         pulp.lpSum(flow_vars[(k, i)] for i in range(num_links) if end_nodes[i] == node) == -data_rates[k], 
                         f"Flow_Conservation_Destination_{k}_Node_{node}")
        else:
            problem += (pulp.lpSum(flow_vars[(k, i)] for i in range(num_links) if start_nodes[i] == node) -
                         pulp.lpSum(flow_vars[(k, i)] for i in range(num_links) if end_nodes[i] == node) == 0, 
                         f"Flow_Conservation_Intermediate_{k}_Node_{node}")

#### Capacity Constraints
for i in range(num_links):
    problem += (pulp.lpSum(flow_vars[(k, i)] for k in range(num_flow_reqs)) <= capacities[i], 
                          f"Capacity_Constraint_Link_{i}")

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

