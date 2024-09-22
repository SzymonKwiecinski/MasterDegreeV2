import pulp

# Define the data from the JSON input
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

# Create the problem
problem = pulp.LpProblem("Communication_Network_Optimization", pulp.LpMinimize)

# Create decision variables
x = pulp.LpVariable.dicts("Flow", 
                           ((i, j, k) for (i, j) in zip(data['StartNode'], data['EndNode']) 
                            for k in range(data['NumFlowReqs'])), 
                           lowBound=0)

# Objective function
problem += pulp.lpSum(data['Cost'][a] * x[(data['StartNode'][a], data['EndNode'][a], k)]
                      for a in range(data['NumLinks']) 
                      for k in range(data['NumFlowReqs'])), "Total_Cost"

# Flow conservation constraints
for i in range(1, 5):  # Assuming node indices start from 1 to 4
    for k in range(data['NumFlowReqs']):
        problem += (pulp.lpSum(x[(data['StartNode'][a], data['EndNode'][a], k)]
                                for a in range(data['NumLinks']) if data['StartNode'][a] == i) 
                     - pulp.lpSum(x[(data['StartNode'][a], data['EndNode'][a], k)]
                                  for a in range(data['NumLinks']) if data['EndNode'][a] == i) 
                     == (data['DataRate'][k] if i == data['Source'][k] 
                         else -data['DataRate'][k] if i == data['Destination'][k] 
                         else 0), f"Flow_Conservation_Node_{i}_FlowReq_{k}")

# Capacity constraints
for a in range(data['NumLinks']):
    problem += (pulp.lpSum(x[(data['StartNode'][a], data['EndNode'][a], k)] for k in range(data['NumFlowReqs'])) <= data['Capacity'][a]), f"Capacity_Constraint_{a}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')