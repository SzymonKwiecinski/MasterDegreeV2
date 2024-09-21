import pulp

# Load data
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Number of power plants (P) and cities (C)
P = len(data['supply'])
C = len(data['demand'])

# Create the LP problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Decision variables: x_pc (electricity transmitted from plant p to city c)
x = pulp.LpVariable.dicts("x", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

# Objective function: Minimize total transmission cost
problem += pulp.lpSum(data['transmission_costs'][p][c] * x[(p, c)] for p in range(P) for c in range(C))

# Constraints

# Supply constraints: Each power plant cannot exceed its supply capacity
for p in range(P):
    problem += pulp.lpSum(x[(p, c)] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_Plant_{p}"

# Demand constraints: Each city must receive its demand
for c in range(C):
    problem += pulp.lpSum(x[(p, c)] for p in range(P)) == data['demand'][c], f"Demand_Constraint_City_{c}"

# Solve the LP problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')