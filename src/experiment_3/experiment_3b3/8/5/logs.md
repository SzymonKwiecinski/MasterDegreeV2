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

\subsection*{Notation}
\begin{itemize}
    \item Let \( n \) be the number of nodes in the communication network.
    \item Let \( A \) be the set of all links in the network, where a link is represented as an ordered pair \( (i, j) \).
    \item Let \( U_{i,j} \) be the maximum capacity (in bits per second) of the link \( (i, j) \).
    \item Let \( C_{i,j} \) be the cost per bit transmitted along the link \( (i, j) \).
    \item Let \( B_{k,l} \) be the data generation rate (in bits per second) from node \( k \) to destination node \( l \).
\end{itemize}

\subsection*{Decision Variables}
Let \( x_{i,j} \) be the flow of data (in bits per second) transmitted along the link \( (i, j) \).

\subsection*{Objective Function}
We aim to minimize the total cost of transmission:
\[
\text{Minimize} \quad Z = \sum_{(i,j) \in A} C_{i,j} \cdot x_{i,j}
\]

\subsection*{Constraints}
1. **Flow Capacity Constraint**: The flow along each link cannot exceed its capacity:
   \[
   x_{i,j} \leq U_{i,j}, \quad \forall (i,j) \in A
   \]

2. **Flow Conservation Constraint**: For each node \( k \) (except for source and destination nodes), the flow in must equal the flow out:
   \[
   \sum_{j: (k,j) \in A} x_{k,j} - \sum_{i: (i,k) \in A} x_{i,k} = 0, \quad \forall k \text{ where } k \text{ is not a source or destination node}
   \]

3. **Supply Constraint**: The flow originating from a source node to its destination must equal the rate of data generation:
   \[
   \sum_{j: (k,j) \in A} x_{k,j} = B_{k,l}, \quad \forall k, l \text{ where } k \text{ is a source node}
   \]

4. **Demand Constraint**: The flow into a destination node must match the total data rate required to be delivered:
   \[
   \sum_{i: (i,l) \in A} x_{i,l} = \sum_{k} B_{k,l}, \quad \forall l \text{ where } l \text{ is a destination node}
   \]

5. **Non-negativity Constraint**: The flow on each link must be non-negative:
   \[
   x_{i,j} \geq 0, \quad \forall (i,j) \in A
   \]

\subsection*{Output Variables}
\begin{itemize}
    \item \( \text{total\_cost} \): The total cost of all the paths.
    \item \( \text{path\_cost} \): The cost associated with each specific path.
    \item \( \text{path\_flow} \): The flow going through each corresponding path.
\end{itemize}

\subsection*{Output Format}
The output should be structured as follows:
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
            for id in 1, ..., m 
        ],
    "total_cost": "total_cost"
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

\subsection*{Notation}
\begin{itemize}
    \item Let \( n \) be the number of nodes in the communication network.
    \item Let \( A \) be the set of all links in the network, where a link is represented as an ordered pair \( (i, j) \).
    \item Let \( U_{i,j} \) be the maximum capacity (in bits per second) of the link \( (i, j) \).
    \item Let \( C_{i,j} \) be the cost per bit transmitted along the link \( (i, j) \).
    \item Let \( B_{k,l} \) be the data generation rate (in bits per second) from node \( k \) to destination node \( l \).
\end{itemize}

\subsection*{Decision Variables}
Let \( x_{i,j} \) be the flow of data (in bits per second) transmitted along the link \( (i, j) \).

\subsection*{Objective Function}
We aim to minimize the total cost of transmission:
\[
\text{Minimize} \quad Z = \sum_{(i,j) \in A} C_{i,j} \cdot x_{i,j}
\]

\subsection*{Constraints}
1. **Flow Capacity Constraint**: The flow along each link cannot exceed its capacity:
   \[
   x_{i,j} \leq U_{i,j}, \quad \forall (i,j) \in A
   \]

2. **Flow Conservation Constraint**: For each node \( k \) (except for source and destination nodes), the flow in must equal the flow out:
   \[
   \sum_{j: (k,j) \in A} x_{k,j} - \sum_{i: (i,k) \in A} x_{i,k} = 0, \quad \forall k \text{ where } k \text{ is not a source or destination node}
   \]

3. **Supply Constraint**: The flow originating from a source node to its destination must equal the rate of data generation:
   \[
   \sum_{j: (k,j) \in A} x_{k,j} = B_{k,l}, \quad \forall k, l \text{ where } k \text{ is a source node}
   \]

4. **Demand Constraint**: The flow into a destination node must match the total data rate required to be delivered:
   \[
   \sum_{i: (i,l) \in A} x_{i,l} = \sum_{k} B_{k,l}, \quad \forall l \text{ where } l \text{ is a destination node}
   \]

5. **Non-negativity Constraint**: The flow on each link must be non-negative:
   \[
   x_{i,j} \geq 0, \quad \forall (i,j) \in A
   \]

\subsection*{Output Variables}
\begin{itemize}
    \item \( \text{total\_cost} \): The total cost of all the paths.
    \item \( \text{path\_cost} \): The cost associated with each specific path.
    \item \( \text{path\_flow} \): The flow going through each corresponding path.
\end{itemize}

\subsection*{Output Format}
The output should be structured as follows:
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
            for id in 1, ..., m 
        ],
    "total_cost": "total_cost"
}
\end{verbatim}

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

#### Unpack data
num_links = data['NumLinks']
start_nodes = data['StartNode']
end_nodes = data['EndNode']
capacities = data['Capacity']
costs = data['Cost']
num_flow_reqs = data['NumFlowReqs']
sources = data['Source']
destinations = data['Destination']
data_rates = data['DataRate']

#### Initialize the problem
problem = pulp.LpProblem("Communication_Network_Optimization", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("Flow", [(i, j) for i, j in zip(start_nodes, end_nodes)], lowBound=0)

#### Objective function
problem += pulp.lpSum([costs[idx] * x[(start_nodes[idx], end_nodes[idx])] for idx in range(num_links)])

#### Constraints
#### Capacity constraints
for idx in range(num_links):
    problem += x[(start_nodes[idx], end_nodes[idx])] <= capacities[idx]

#### Flow conservation constraints
all_nodes = set(start_nodes).union(set(end_nodes))
intermediate_nodes = all_nodes.difference(set(sources + destinations))

for k in intermediate_nodes:
    inflow = pulp.lpSum([x[(i, k)] for i in start_nodes if (i, k) in x])
    outflow = pulp.lpSum([x[(k, j)] for j in end_nodes if (k, j) in x])
    problem += inflow == outflow

#### Supply constraints for source nodes
for idx, (source, dest) in enumerate(zip(sources, destinations)):
    outflow = pulp.lpSum([x[(source, j)] for j in end_nodes if (source, j) in x])
    problem += outflow == data_rates[idx]

#### Demand constraints for destination nodes
for destination in destinations:
    inflow = pulp.lpSum([x[(i, destination)] for i in start_nodes if (i, destination) in x])
    total_data_rate_to_destination = sum(data_rates[idx] for idx, dest in enumerate(destinations) if dest == destination)
    problem += inflow == total_data_rate_to_destination

#### Solve the problem
problem.solve()

#### Prepare output
optimized_paths = []
for idx in range(num_flow_reqs):
    source = sources[idx]
    destination = destinations[idx]
    path_flow = 0
    path_cost = 0
    current_node = source
    route = [current_node]

    while current_node != destination:
        for next_node in end_nodes:
            if (current_node, next_node) in x and pulp.value(x[(current_node, next_node)]) > 0:
                path_flow = pulp.value(x[(current_node, next_node)])
                path_cost += costs[start_nodes.index(current_node)] * path_flow
                current_node = next_node
                route.append(current_node)
                break
    
    optimized_paths.append({
        "source": source,
        "destination": destination,
        "route": route,
        "path_flow": path_flow,
        "path_cost": path_cost
    })

total_cost = pulp.value(problem.objective)

#### Output JSON
output_data = {
    "optimized_paths": {
        "paths": optimized_paths,
        "total_cost": total_cost
    }
}

import json
print(json.dumps(output_data, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

