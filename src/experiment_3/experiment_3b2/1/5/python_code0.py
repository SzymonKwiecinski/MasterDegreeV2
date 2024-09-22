import pulp
import json

# Data
data = json.loads('{"NumLinks": 4, "StartNode": [1, 2, 2, 3], "EndNode": [2, 3, 4, 4], "Capacity": [50, 40, 60, 50], "Cost": [2, 3, 1, 1], "NumFlowReqs": 2, "Source": [1, 2], "Destination": [4, 3], "DataRate": [40, 30]}')

# Create a linear programming problem
problem = pulp.LpProblem("NetworkFlow", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("Flow", ((data['StartNode'][i], data['EndNode'][i], k, l) 
                                     for i in range(data['NumLinks']) 
                                     for k in range(data['NumFlowReqs']) 
                                     for l in range(data['NumFlowReqs'])), 
                                   lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['Cost'][i] * x[(data['StartNode'][i], data['EndNode'][i], k, l)] 
                       for i in range(data['NumLinks'])
                       for k in range(data['NumFlowReqs'])
                       for l in range(data['NumFlowReqs'])), "Total_Cost"

# Capacity Constraints
for i in range(data['NumLinks']):
    problem += pulp.lpSum(x[(data['StartNode'][i], data['EndNode'][i], k, l)] 
                          for k in range(data['NumFlowReqs']) 
                          for l in range(data['NumFlowReqs'])) <= data['Capacity'][i], f"Capacity_{i}"

# Flow Conservation Constraints
for k in range(data['NumFlowReqs']):
    for node in range(1, 5):  # Nodes are 1 to 4
        inflow = pulp.lpSum(x[(j, node, k, l) for j in range(1, 5) if (j, node) in zip(data['StartNode'], data['EndNode'])] 
                            for l in range(data['NumFlowReqs']))
        outflow = pulp.lpSum(x[(node, j, k, l) for j in range(1, 5) if (node, j) in zip(data['StartNode'], data['EndNode'])] 
                             for l in range(data['NumFlowReqs']))
        
        if node == data['Source'][k]:
            problem += inflow - outflow == data['DataRate'][k], f"FlowConservation_Influx_{node}_{k}"
        elif node == data['Destination'][k]:
            problem += inflow - outflow == -data['DataRate'][k], f"FlowConservation_Outflux_{node}_{k}"
        else:
            problem += inflow - outflow == 0, f"FlowConservation_Network_{node}_{k}"

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')