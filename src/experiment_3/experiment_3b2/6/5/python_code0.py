import pulp

# Data from JSON format
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

# Problem Definition
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Flow", 
                           ((k, l, i, j) for k in range(data['NumFlowReqs']) 
                                         for l in range(data['NumFlowReqs']) 
                                         for i in range(data['NumLinks']) 
                                         for j in range(data['NumLinks'])), 
                           lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['Cost'][i] * x[k, l, i, j] 
                       for k in range(data['NumFlowReqs']) 
                       for l in range(data['NumFlowReqs']) 
                       for i in range(data['NumLinks']) 
                       for j in range(data['NumLinks'])), "Total_Transmission_Cost"

# Flow Conservation Constraints
for m in range(1, 5):  # Assuming node indices from 1 to 4
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

# Capacity Constraints
for i in range(data['NumLinks']):
    problem += pulp.lpSum(x[k, l, i, j] for k in range(data['NumFlowReqs']) 
                           for l in range(data['NumFlowReqs']) 
                           for j in range(data['NumLinks']) 
                           if data['StartNode'][i] == data['StartNode'][j] and data['EndNode'][i] == data['EndNode'][j]) <= \
               data['Capacity'][i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')