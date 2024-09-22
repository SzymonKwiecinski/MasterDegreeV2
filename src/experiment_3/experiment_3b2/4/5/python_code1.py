import pulp
import json

# Load data
data = json.loads('{"NumLinks": 4, "StartNode": [1, 2, 2, 3], "EndNode": [2, 3, 4, 4], "Capacity": [50, 40, 60, 50], "Cost": [2, 3, 1, 1], "NumFlowReqs": 2, "Source": [1, 2], "Destination": [4, 3], "DataRate": [40, 30]}')

# Model initialization
problem = pulp.LpProblem("Network_Flow_Optimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("flow", ((i, j, k, l) for i in range(data['NumLinks']) 
                                     for j in range(data['NumFlowReqs']) 
                                     for k in range(2) 
                                     for l in range(2)), lowBound=0)

# Objective function
problem += pulp.lpSum(data['Cost'][i] * x[i, j, k, l]
                       for i in range(data['NumLinks'])
                       for j in range(data['NumFlowReqs'])
                       for k in range(2)
                       for l in range(2)), "Total_Cost"

# Flow Conservation Constraints
for k in range(data['NumFlowReqs']):
    for m in range(1, 5):  # Assuming nodes are numbered from 1 to 4
        inflow = pulp.lpSum(x[i, j, k, l] for i in range(data['NumLinks']) 
                            for l in range(2) if data['EndNode'][i] == m)
        outflow = pulp.lpSum(x[i, j, k, l] for i in range(data['NumLinks']) 
                             for l in range(2) if data['StartNode'][i] == m)
        
        if m == data['Source'][k]:
            problem += inflow - outflow == data['DataRate'][k], f"Flow_Conservation_Req_{k}_Node_{m}"
        elif m == data['Destination'][k]:
            problem += inflow - outflow == -data['DataRate'][k], f"Flow_Conservation_Req_{k}_Node_{m}"
        else:
            problem += inflow - outflow == 0, f"Flow_Conservation_Req_{k}_Node_{m}"

# Capacity constraints
for i in range(data['NumLinks']):
    problem += pulp.lpSum(x[i, j, k, l] for j in range(data['NumFlowReqs']) for k in range(2) for l in range(2)) <= data['Capacity'][i], f"Capacity_Constraint_Link_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')