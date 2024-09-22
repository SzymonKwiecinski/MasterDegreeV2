import pulp

# Data extraction from JSON format
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

# Indices
P = len(data['supply'])  # Number of power plants
C = len(data['demand'])   # Number of cities

# Initialize the problem
problem = pulp.LpProblem("ElectricityDistribution", pulp.LpMinimize)

# Decision Variables: send_{p,c}
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[p][c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Supply Constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_{p}"

# Demand Constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) >= data['demand'][c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Output the results
for p in range(P):
    for c in range(C):
        print(f'Send from power plant {p+1} to city {c+1}: {send[p][c].varValue} million kWh')

total_cost = pulp.value(problem.objective)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')