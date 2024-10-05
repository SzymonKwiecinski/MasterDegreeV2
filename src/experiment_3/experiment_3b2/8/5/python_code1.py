import pulp

# Data input from the provided JSON format
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

# Create a linear programming problem
problem = pulp.LpProblem("CommunicationNetworkOptimization", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("Flow", 
                           ((i, j, k, l) for i in range(data['NumLinks']) 
                            for k in range(data['NumFlowReqs']) 
                            for l in range(data['NumFlowReqs'])), 
                           lowBound=0, 
                           cat='Continuous')

# Objective function
problem += pulp.lpSum(data['Cost'][i] * x[(i, j, k, l)] 
                       for i in range(data['NumLinks']) 
                       for k in range(data['NumFlowReqs']) 
                       for l in range(data['NumFlowReqs']) 
                       if data['StartNode'][i] == data['Source'][k] 
                       and data['EndNode'][i] == data['Destination'][l]), "Total_Cost"

# Flow conservation constraints
for i in range(1, max(data['StartNode']) + 1):
    for k in range(data['NumFlowReqs']):
        problem += (pulp.lpSum(x[(i, j, k, l)] for j in range(data['NumLinks']) 
                                 if data['StartNode'][j] == i) - 
                      pulp.lpSum(x[(j, i, k, l)] for j in range(data['NumLinks']) 
                                 if data['EndNode'][j] == i) == 
                      (data['DataRate'][k] if i == data['Source'][k] else
                       -data['DataRate'][k] if i == data['Destination'][k] else 0)), f"FlowConservation_{i}_{k}"

# Capacity constraints
for i in range(data['NumLinks']):
    problem += (pulp.lpSum(x[(i, j, k, l)] for j in range(data['NumFlowReqs']) 
                            for k in range(data['NumFlowReqs'])) <= data['Capacity'][i]), f"Capacity_{i}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')