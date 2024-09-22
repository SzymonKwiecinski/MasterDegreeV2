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
The problem presented involves optimizing the data flow through a communication network while minimizing transmission costs. This is a typical network flow problem that can be modeled as a linear programming (LP) problem. The objective is to determine the flow of data between nodes using designated paths while respecting the capacity constraints of each link and minimizing the total cost.

Below is the mathematical model of the problem in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Network Flow Optimization}

\subsection*{Sets and Indices}
\begin{itemize}
    \item Let \( N \) denote the set of nodes.
    \item Let \( A \) denote the set of links, where each link is represented as a pair \((i, j)\).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( U_{i,j} \): Capacity of link \((i, j)\), i.e., maximum number of bits per second it can carry.
    \item \( C_{i,j} \): Cost per bit transmitted along link \((i, j)\).
    \item \( B_{k,l} \): Data generation rate from node \(k\) to node \(l\), in bits per second.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_{i,j}^{k,l} \): Flow of data from node \(k\) to node \(l\) through link \((i, j)\).
\end{itemize}

\subsection*{Objective Function}
The objective is to minimize the total transmission cost:
\[
\min \sum_{(i,j) \in A} \sum_{(k,l) \in N \times N} C_{i,j} \cdot x_{i,j}^{k,l}
\]

\subsection*{Constraints}
\begin{enumerate}
    \item \textbf{Flow Conservation:} For each node \(m\) and data pair \((k, l)\):
    \[
    \sum_{j : (m, j) \in A} x_{m,j}^{k,l} - \sum_{i : (i, m) \in A} x_{i,m}^{k,l} =
    \begin{cases} 
    B_{k,l}, & \text{if } m = k \\
    -B_{k,l}, & \text{if } m = l \\
    0, & \text{otherwise}
    \end{cases}
    \]
    
    \item \textbf{Capacity Constraints:} For each link \((i, j)\):
    \[
    \sum_{(k,l) \in N \times N} x_{i,j}^{k,l} \leq U_{i,j}
    \]
    
    \item \textbf{Non-Negativity:} 
    \[
    x_{i,j}^{k,l} \geq 0, \quad \forall (i,j) \in A, \forall (k,l) \in N \times N
    \]
\end{enumerate}

\end{document}
```

This model defines the flow of data with the goal of minimizing transmission costs across the network, subject to capacity and flow conservation constraints. The decision variables represent the flow of data between specific origins and destinations through specific links. The constraints ensure the feasibility of these flows in the context of the network's physical and operational limitations.

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

\subsection*{Sets and Indices}
\begin{itemize}
    \item Let \( N \) denote the set of nodes.
    \item Let \( A \) denote the set of links, where each link is represented as a pair \((i, j)\).
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( U_{i,j} \): Capacity of link \((i, j)\), i.e., maximum number of bits per second it can carry.
    \item \( C_{i,j} \): Cost per bit transmitted along link \((i, j)\).
    \item \( B_{k,l} \): Data generation rate from node \(k\) to node \(l\), in bits per second.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( x_{i,j}^{k,l} \): Flow of data from node \(k\) to node \(l\) through link \((i, j)\).
\end{itemize}

\subsection*{Objective Function}
The objective is to minimize the total transmission cost:
\[
\min \sum_{(i,j) \in A} \sum_{(k,l) \in N \times N} C_{i,j} \cdot x_{i,j}^{k,l}
\]

\subsection*{Constraints}
\begin{enumerate}
    \item \textbf{Flow Conservation:} For each node \(m\) and data pair \((k, l)\):
    \[
    \sum_{j : (m, j) \in A} x_{m,j}^{k,l} - \sum_{i : (i, m) \in A} x_{i,m}^{k,l} =
    \begin{cases} 
    B_{k,l}, & \text{if } m = k \\
    -B_{k,l}, & \text{if } m = l \\
    0, & \text{otherwise}
    \end{cases}
    \]
    
    \item \textbf{Capacity Constraints:} For each link \((i, j)\):
    \[
    \sum_{(k,l) \in N \times N} x_{i,j}^{k,l} \leq U_{i,j}
    \]
    
    \item \textbf{Non-Negativity:} 
    \[
    x_{i,j}^{k,l} \geq 0, \quad \forall (i,j) \in A, \forall (k,l) \in N \times N
    \]
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 'DataRate': [40, 30]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = json.loads('{"NumLinks": 4, "StartNode": [1, 2, 2, 3], "EndNode": [2, 3, 4, 4], "Capacity": [50, 40, 60, 50], "Cost": [2, 3, 1, 1], "NumFlowReqs": 2, "Source": [1, 2], "Destination": [4, 3], "DataRate": [40, 30]}')

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

#### Sets and indices
nodes = list(set(sources + destinations))
links = [(start_nodes[i], end_nodes[i]) for i in range(num_links)]

#### Create the problem
problem = pulp.LpProblem("Network_Flow_Optimization", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("flow", ((i, j, k, l) for (i, j) in links for k in sources for l in destinations), lowBound=0)

#### Objective Function
problem += pulp.lpSum(costs[start_nodes.index(i)] * x[i, j, k, l] for (i, j) in links for k in sources for l in destinations), "Total_Transmission_Cost"

#### Flow Conservation Constraints
for m in nodes:
    for k in sources:
        for l in destinations:
            if m == k:
                problem += pulp.lpSum(x[i, j, k, l] for (i, j) in links if i == m) - pulp.lpSum(x[i, j, k, l] for (i, j) in links if j == m) == data_rates[sources.index(k)], f"FlowConservation_Src_{k}_Dest_{l}_Node_{m}"
            elif m == l:
                problem += pulp.lpSum(x[i, j, k, l] for (i, j) in links if i == m) - pulp.lpSum(x[i, j, k, l] for (i, j) in links if j == m) == -data_rates[sources.index(k)], f"FlowConservation_Src_{k}_Dest_{l}_Node_{m}"
            else:
                problem += pulp.lpSum(x[i, j, k, l] for (i, j) in links if i == m) - pulp.lpSum(x[i, j, k, l] for (i, j) in links if j == m) == 0, f"FlowConservation_Src_{k}_Dest_{l}_Node_{m}"

#### Capacity Constraints
for (i, j) in links:
    problem += pulp.lpSum(x[i, j, k, l] for k in sources for l in destinations) <= capacities[start_nodes.index(i)], f"Capacity_Constraint_{i}_{j}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

