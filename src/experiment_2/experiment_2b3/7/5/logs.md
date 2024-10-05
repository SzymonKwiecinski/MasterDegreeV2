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

#### Data input from JSON
input_data = {
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

#### Unpack the data
links = [{'start': input_data['StartNode'][i], 'end': input_data['EndNode'][i],
          'U': input_data['Capacity'][i], 'C': input_data['Cost'][i]} for i in range(input_data['NumLinks'])]
data_flows = [{'source': input_data['Source'][i], 'destination': input_data['Destination'][i],
               'rate': input_data['DataRate'][i]} for i in range(input_data['NumFlowReqs'])]

#### Prepare the LP problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

#### Define variables
flow_vars = {}
for link in links:
    for flow_req in data_flows:
        #### Variable for flow through link (i, j) for data from source k to destination l
        flow_vars[(link['start'], link['end'], flow_req['source'], flow_req['destination'])] = pulp.LpVariable(
            f'flow_{link["start"]}_{link["end"]}_{flow_req["source"]}_{flow_req["destination"]}', lowBound=0)

#### Objective function: Minimize total cost
problem += pulp.lpSum(link['C'] * flow_vars[(link['start'], link['end'], flow_req['source'], flow_req['destination'])]
                      for link in links for flow_req in data_flows), "Total_Cost"

#### Constraints
#### Capacity constraints
for link in links:
    problem += pulp.lpSum(flow_vars[(link['start'], link['end'], flow_req['source'], flow_req['destination'])]
                          for flow_req in data_flows) <= link['U'], f'capacity_{link["start"]}_{link["end"]}'

#### Flow conservation constraints
for flow_req in data_flows:
    nodes = set([link['start'] for link in links] + [link['end'] for link in links])
    for node in nodes:
        flow_in = pulp.lpSum(flow_vars[(j, node, flow_req['source'], flow_req['destination'])]
                             for j in [link['start'] for link in links if link['end'] == node])
        flow_out = pulp.lpSum(flow_vars[(node, j, flow_req['source'], flow_req['destination'])]
                              for j in [link['end'] for link in links if link['start'] == node])

        if node == flow_req['source']:  #### Source node
            problem += flow_out - flow_in == flow_req['rate'], f'flow_conservation_source_{node}_{flow_req["source"]}_{flow_req["destination"]}'
        elif node == flow_req['destination']:  #### Destination node
            problem += flow_out - flow_in == -flow_req['rate'], f'flow_conservation_dest_{node}_{flow_req["source"]}_{flow_req["destination"]}'
        else:  #### Intermediate node
            problem += flow_out - flow_in == 0, f'flow_conservation_intermediate_{node}_{flow_req["source"]}_{flow_req["destination"]}'

#### Solve the problem
problem.solve()

#### Output formatting
optimized_paths = {'paths': [], 'total_cost': pulp.value(problem.objective)}

for flow_req in data_flows:
    for link in links:
        flow_value = pulp.value(flow_vars[(link['start'], link['end'], flow_req['source'], flow_req['destination'])])
        if flow_value > 0:
            optimized_paths['paths'].append({
                'source': flow_req['source'],
                'destination': flow_req['destination'],
                'route': [link['start'], link['end']],
                'path_flow': flow_value,
                'path_cost': flow_value * link['C']
            })

print(optimized_paths)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

