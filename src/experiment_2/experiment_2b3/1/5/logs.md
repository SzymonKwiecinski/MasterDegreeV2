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

#### Data from JSON
data = {'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 'DataRate': [40, 30]}

#### Unpack the data
num_links = data['NumLinks']
start_node = data['StartNode']
end_node = data['EndNode']
capacity = data['Capacity']
cost = data['Cost']
num_flow_reqs = data['NumFlowReqs']
source = data['Source']
destination = data['Destination']
data_rate = data['DataRate']

#### Possible paths for each flow request
links = [(start_node[i], end_node[i]) for i in range(num_links)]

#### Problem definition
problem = pulp.LpProblem("Minimize_Total_Transmission_Cost", pulp.LpMinimize)

#### Decision variables for flow on each link for each flow request
flow_vars = {}
for f in range(num_flow_reqs):
    for (i, j) in links:
        flow_vars[f, (i, j)] = pulp.LpVariable(f'flow_{f}_{i}_{j}', lowBound=0, upBound=capacity[links.index((i, j))], cat='Continuous')

#### Objective function
problem += pulp.lpSum([flow_vars[f, (i, j)] * cost[links.index((i, j))] for f in range(num_flow_reqs) for (i, j) in links])

#### Constraints
for f in range(num_flow_reqs):
    #### Flow conservation
    for node in set(start_node + end_node):
        incoming = pulp.lpSum([flow_vars[f, (i, j)] for (i, j) in links if j == node])
        outgoing = pulp.lpSum([flow_vars[f, (i, j)] for (i, j) in links if i == node])
        
        if node == source[f]:
            problem += (outgoing - incoming == data_rate[f], f'flow_conservation_source_{f}_{node}')
        elif node == destination[f]:
            problem += (incoming - outgoing == data_rate[f], f'flow_conservation_dest_{f}_{node}')
        else:
            problem += (incoming == outgoing, f'flow_conservation_middle_{f}_{node}')

#### Solve the problem
problem.solve()

#### Collect results
optimized_paths = {"paths": []}
total_cost = pulp.value(problem.objective)

for f in range(num_flow_reqs):
    path_flow = {}
    for (i, j) in links:
        if pulp.value(flow_vars[f, (i, j)]) > 0:
            path_flow[(i, j)] = pulp.value(flow_vars[f, (i, j)])
    
    path_cost = sum([pulp.value(flow_vars[f, (i, j)]) * cost[links.index((i, j))] for (i, j) in path_flow])
    optimized_paths["paths"].append({
        "source": source[f],
        "destination": destination[f],
        "route": list(path_flow.keys()),
        "path_flow": list(path_flow.values()),
        "path_cost": path_cost
    })

optimized_paths["total_cost"] = total_cost

print(optimized_paths)
print(f'(Objective Value): <OBJ>{total_cost}</OBJ>')
```

