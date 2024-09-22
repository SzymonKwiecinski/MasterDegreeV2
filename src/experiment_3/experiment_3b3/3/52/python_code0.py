import pulp

# Data
data = {
    'supply': [30, 25, 45], 
    'demand': [40, 60], 
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Number of power plants and cities
P = len(data['supply'])
C = len(data['demand'])

# Problem
problem = pulp.LpProblem("Electric_Utility_Cost_Minimization", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("Send", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[p, c] for p in range(P) for c in range(C))

# Supply Constraints
for p in range(P):
    problem += pulp.lpSum(send[p, c] for c in range(C)) <= data['supply'][p]

# Demand Constraints
for c in range(C):
    problem += pulp.lpSum(send[p, c] for p in range(P)) == data['demand'][c]

# Solve the problem
problem.solve()

# Output results
for p in range(P):
    for c in range(C):
        print(f"Electricity sent from plant {p} to city {c}: {send[p, c].varValue} million kWh")

print(f'Total Transmission Cost (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')