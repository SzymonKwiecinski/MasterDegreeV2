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

We are given a communication network with \( n \) nodes and a set of directed communication links \( A \), where each link \( (i,j) \in A \) can carry up to \( U_{i,j} \) bits per second at a cost of \( C_{i,j} \) per bit. We need to determine the optimal paths for transmitting data from source nodes to destination nodes while minimizing the total transmission cost.

To model the problem as a linear programming (LP) problem, we define the following decision variables:

\[
x_{k,l}^{i,j} : \text{the flow of data from source node } k \text{ to destination node } l \text{ through link } (i,j).
\]

Objective function:
Minimize the total cost of transmitting all data, which is given by:

\[
\min \sum_{(i,j) \in A} \sum_{k,l} C_{i,j} \cdot x_{k,l}^{i,j}
\]

Subject to the constraints:

1. **Flow conservation constraints:**

   For each node \( m \) that is not a source or destination for any data:

   \[
   \sum_{j: (m,j) \in A} x_{k,l}^{m,j} - \sum_{i: (i,m) \in A} x_{k,l}^{i,m} = 
   \begin{cases} 
   B_{k,l}, & \text{if } m = k \\
   -B_{k,l}, & \text{if } m = l \\
   0, & \text{otherwise}
   \end{cases}
   \]

2. **Capacity constraints:**

   For each link \( (i,j) \in A \):

   \[
   \sum_{k,l} x_{k,l}^{i,j} \leq U_{i,j}
   \]

3. **Non-negativity constraints:**

   \[
   x_{k,l}^{i,j} \geq 0 \quad \forall k,l,i,j
   \]

This linear programming formulation ensures that the data is routed in such a way that the total cost is minimized, while satisfying the demands at each source node and adhering to the capacity constraints on each link.

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

We are given a communication network with \( n \) nodes and a set of directed communication links \( A \), where each link \( (i,j) \in A \) can carry up to \( U_{i,j} \) bits per second at a cost of \( C_{i,j} \) per bit. We need to determine the optimal paths for transmitting data from source nodes to destination nodes while minimizing the total transmission cost.

To model the problem as a linear programming (LP) problem, we define the following decision variables:

\[
x_{k,l}^{i,j} : \text{the flow of data from source node } k \text{ to destination node } l \text{ through link } (i,j).
\]

Objective function:
Minimize the total cost of transmitting all data, which is given by:

\[
\min \sum_{(i,j) \in A} \sum_{k,l} C_{i,j} \cdot x_{k,l}^{i,j}
\]

Subject to the constraints:

1. **Flow conservation constraints:**

   For each node \( m \) that is not a source or destination for any data:

   \[
   \sum_{j: (m,j) \in A} x_{k,l}^{m,j} - \sum_{i: (i,m) \in A} x_{k,l}^{i,m} = 
   \begin{cases} 
   B_{k,l}, & \text{if } m = k \\
   -B_{k,l}, & \text{if } m = l \\
   0, & \text{otherwise}
   \end{cases}
   \]

2. **Capacity constraints:**

   For each link \( (i,j) \in A \):

   \[
   \sum_{k,l} x_{k,l}^{i,j} \leq U_{i,j}
   \]

3. **Non-negativity constraints:**

   \[
   x_{k,l}^{i,j} \geq 0 \quad \forall k,l,i,j
   \]

This linear programming formulation ensures that the data is routed in such a way that the total cost is minimized, while satisfying the demands at each source node and adhering to the capacity constraints on each link.

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

#### Problem Definition
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("Flow", 
                           ((k, l, i, j) for k in range(data['NumFlowReqs']) 
                                         for l in range(data['NumFlowReqs']) 
                                         for i in range(data['NumLinks']) 
                                         for j in range(data['NumLinks'])), 
                           lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(data['Cost'][i] * x[k, l, i, j] 
                       for k in range(data['NumFlowReqs']) 
                       for l in range(data['NumFlowReqs']) 
                       for i in range(data['NumLinks']) 
                       for j in range(data['NumLinks'])), "Total_Transmission_Cost"

#### Flow Conservation Constraints
for m in range(1, 5):  #### Assuming node indices from 1 to 4
    for k in range(data['NumFlowReqs']):
        for l in range(data['NumFlowReqs']):
            if m == data['Source'][k]:
                problem += pulp.lpSum(x[k, l, i, j] for i in range(data['NumLinks']) 
                                       if data['StartNode'][i] == m for j in range(data['NumLinks'])) == data['DataRate'][k]
            elif m == data['Destination'][l]:
                problem += pulp.lpSum(x[k, l, i, j] for i in range(data['NumLinks']) 
                                       if data['EndNode'][i] == m for j in range(data['NumLinks'])) == -data['DataRate'][k]
            else:
                problem += pulp.lpSum(x[k, l, i, j] for i in range(data['NumLinks']) 
                                       if data['StartNode'][i] == m for j in range(data['NumLinks'])) - \
                           pulp.lpSum(x[k, l, i, j] for i in range(data['NumLinks']) 
                                       if data['EndNode'][i] == m for j in range(data['NumLinks'])) == 0

#### Capacity Constraints
for i in range(data['NumLinks']):
    problem += pulp.lpSum(x[k, l, i, j] for k in range(data['NumFlowReqs']) 
                           for l in range(data['NumFlowReqs']) 
                           for j in range(data['NumLinks']) 
                           if data['StartNode'][i] == data['StartNode'][j] and data['EndNode'][i] == data['EndNode'][j]) <= \
               data['Capacity'][i]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

