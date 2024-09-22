# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
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
<DATA>
{'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 'DataRate': [40, 30]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extract inputs from JSON data format
data = {'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 'DataRate': [40, 30]}

#### Initialize the LP problem
problem = pulp.LpProblem("NetworkFlowMinCost", pulp.LpMinimize)

#### Define sets and parameters
links = [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])]
U = {links[i]: data['Capacity'][i] for i in range(data['NumLinks'])}
C = {links[i]: data['Cost'][i] for i in range(data['NumLinks'])}

source_nodes = data['Source']
destination_nodes = data['Destination']
data_rates = data['DataRate']
num_flow_reqs = data['NumFlowReqs']

#### Define decision variables
flow = pulp.LpVariable.dicts("flow", ((s, d, i, j) for s, d in zip(source_nodes, destination_nodes) for i, j in links), lowBound=0)

#### Objective Function
problem += pulp.lpSum(C[i, j] * flow[s, d, i, j] for s, d in zip(source_nodes, destination_nodes) for i, j in links)

#### Capacity Constraints
for i, j in links:
    problem += pulp.lpSum(flow[s, d, i, j] for s, d in zip(source_nodes, destination_nodes)) <= U[i, j]

#### Flow Conservation Constraints
for s, d in zip(source_nodes, destination_nodes):
    for n in set(data['StartNode'] + data['EndNode']):
        if n == s:
            problem += pulp.lpSum(flow[s, d, n, j] for _, j in links if _ == n) - \
                       pulp.lpSum(flow[s, d, i, n] for i, _ in links if _ == n) == data_rates[source_nodes.index(s)]
        elif n == d:
            problem += pulp.lpSum(flow[s, d, i, n] for i, _ in links if _ == n) - \
                       pulp.lpSum(flow[s, d, n, j] for _, j in links if _ == n) == data_rates[source_nodes.index(s)]
        else:
            problem += pulp.lpSum(flow[s, d, n, j] for _, j in links if _ == n) - \
                       pulp.lpSum(flow[s, d, i, n] for i, _ in links if _ == n) == 0

#### Solve the problem
problem.solve()

#### Output the solution in the required format
optimized_paths = {"paths": []}
total_cost = pulp.value(problem.objective)

for s, d in zip(source_nodes, destination_nodes):
    path_details = {"source": s, "destination": d, "route": [], "path_flow": 0, "path_cost": 0}
    for i, j in links:
        if pulp.value(flow[s, d, i, j]) > 0:
            path_details["route"].append(i)
            path_details["path_flow"] += pulp.value(flow[s, d, i, j])
            path_details["path_cost"] += C[i, j] * pulp.value(flow[s, d, i, j])
    path_details["route"].append(d)
    optimized_paths["paths"].append(path_details)

output = {
    "optimized_paths": optimized_paths,
    "total_cost": f"{total_cost}"
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

