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

# Set up the problem
problem = pulp.LpProblem("CommunicationNetwork", pulp.LpMinimize)

# Create decision variables
links = list(range(1, data['NumLinks'] + 1))
x = pulp.LpVariable.dicts("flow", links, lowBound=0)

# Objective function
problem += pulp.lpSum(data['Cost'][i-1] * x[i] for i in links), "Total_Cost"

# Flow balance constraints
for k in range(data['NumFlowReqs']):
    source = data['Source'][k]
    destination = data['Destination'][k]
    flow_rate = data['DataRate'][k]
    
    for node in range(1, max(data['StartNode'] + data['EndNode']) + 1):        
        inflow = pulp.lpSum(x[i] for i in links if data['EndNode'][i-1] == node)
        outflow = pulp.lpSum(x[i] for i in links if data['StartNode'][i-1] == node)

        if node == source:
            problem += outflow - inflow == flow_rate, f"Flow_Balance_Source_{node}_{k}"
        elif node == destination:
            problem += outflow - inflow == -flow_rate, f"Flow_Balance_Destination_{node}_{k}"
        else:
            problem += outflow - inflow == 0, f"Flow_Balance_{node}_{k}"

# Capacity constraints
for i in links:
    problem += x[i] <= data['Capacity'][i - 1], f"Capacity_Constraint_{i}"

# Solve the problem
problem.solve()

# Output the results
for i in links:
    if x[i].varValue > 0:
        print(f'Flow on link {data["StartNode"][i-1]} -> {data["EndNode"][i-1]}: {x[i].varValue} bits')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')