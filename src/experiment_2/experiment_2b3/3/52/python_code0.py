import pulp

# Input Data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Number of power plants and cities
P = len(data['supply'])
C = len(data['demand'])

# Initialize the problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

# Decision Variables
send = [[pulp.LpVariable(f'send_{p}_{c}', lowBound=0) for c in range(C)] for p in range(P)]

# Objective Function
total_cost = pulp.lpSum(data['transmission_costs'][p][c] * send[p][c] for p in range(P) for c in range(C))
problem += total_cost

# Constraints for each power plant
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_Plant_{p}"

# Constraints for each city
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) == data['demand'][c], f"Demand_Constraint_City_{c}"

# Solve the problem
problem.solve()

# Output
output = {
    'send': [[pulp.value(send[p][c]) for c in range(C)] for p in range(P)],
    'total_cost': pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')