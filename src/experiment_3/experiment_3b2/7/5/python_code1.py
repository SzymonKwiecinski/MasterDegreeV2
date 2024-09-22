import pulp
import json

# Load data from the provided JSON format
data = {'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 
        'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 
        'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 
        'DataRate': [40, 30]}

# Create a Linear Programming problem
problem = pulp.LpProblem("Communication_Network_Optimization", pulp.LpMinimize)

# Define sets and parameters
NumLinks = data['NumLinks']
StartNode = data['StartNode']
EndNode = data['EndNode']
Capacity = data['Capacity']
Cost = data['Cost']
NumFlowReqs = data['NumFlowReqs']
Source = data['Source']
Destination = data['Destination']
DataRate = data['DataRate']

# Define decision variables: x_ij^kl
x = pulp.LpVariable.dicts("x", 
                           ((i, j, k, l) for i in range(NumLinks)
                            for j in range(NumLinks)  # Added j here
                            for k in range(NumFlowReqs) 
                            for l in range(NumFlowReqs)), 
                           lowBound=0, cat='Continuous')

# Objective function: Minimize total cost
problem += pulp.lpSum(Cost[i] * x[i, StartNode[i]-1, k, l] 
                       for i in range(NumLinks) 
                       for k in range(NumFlowReqs) 
                       for l in range(NumFlowReqs)), "Total_Cost"

# Flow conservation constraints
for k in range(NumFlowReqs):
    for l in range(NumFlowReqs):
        # For source nodes
        problem += (pulp.lpSum(x[i, StartNode[i]-1, k, l] for i in range(NumLinks) if StartNode[i] == Source[k]) 
                     - pulp.lpSum(x[i, EndNode[i]-1, k, l] for i in range(NumLinks) if EndNode[i] == Source[k]) 
                     == DataRate[k], f"Flow_Conservation_Source_{k}_{l}")

for m in range(1, max(StartNode) + 1):
    if m not in Source:
        for k in range(NumFlowReqs):
            for l in range(NumFlowReqs):
                problem += (pulp.lpSum(x[i, m, k, l] for i in range(NumLinks) if StartNode[i] == m) 
                             - pulp.lpSum(x[i, m, k, l] for i in range(NumLinks) if EndNode[i] == m) 
                             == 0, f"Flow_Conservation_Intermediate_{m}_{k}_{l}")

# For destination nodes
for k in range(NumFlowReqs):
    for l in range(NumFlowReqs):
        problem += (pulp.lpSum(x[i, Destination[l]-1, k, l] for i in range(NumLinks) if EndNode[i] == Destination[l]) 
                     - pulp.lpSum(x[i, StartNode[i]-1, k, l] for i in range(NumLinks) if StartNode[i] == Destination[l]) 
                     == DataRate[l], f"Flow_Conservation_Destination_{k}_{l}")

# Capacity constraints
for i in range(NumLinks):
    for k in range(NumFlowReqs):
        for l in range(NumFlowReqs):
            problem += (pulp.lpSum(x[i, j, k, l] for j in range(NumLinks) if StartNode[i] == StartNode[j]) 
                         <= Capacity[i], f"Capacity_Constraint_{i}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')