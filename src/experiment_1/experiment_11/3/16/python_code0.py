import pulp

# Data from JSON
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Parameters
P = len(data['supply'])  # Number of power plants
C = len(data['demand'])   # Number of cities

# Create the linear programming problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Decision Variables: x_pc - amount of electricity transmitted from power plant p to city c
x = pulp.LpVariable.dicts("x", (range(P), range(C)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['transmission_costs'][p][c] * x[p][c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Constraints
# Supply constraints
for p in range(P):
    problem += pulp.lpSum(x[p][c] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_Plant_{p}"

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(x[p][c] for p in range(P)) == data['demand'][c], f"Demand_Constraint_City_{c}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')