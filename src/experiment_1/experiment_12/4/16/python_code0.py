import pulp

# Data from JSON
data = {
    'supply': [30, 25, 45],
    'demand': [40, 60],
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Number of power plants and cities
P = len(data['supply'])
C = len(data['demand'])

# Supply capacities and demands
supply = data['supply']
demand = data['demand']

# Transmission costs
transmission_costs = data['transmission_costs']

# Initialize the problem
problem = pulp.LpProblem("Electricity Distribution", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((p, c) for p in range(P) for c in range(C)), lowBound=0)

# Objective function: Minimize total transmission cost
problem += pulp.lpSum(transmission_costs[p][c] * x[p, c] for p in range(P) for c in range(C))

# Constraints

# 1. Supply capacity constraints for each power plant
for p in range(P):
    problem += pulp.lpSum(x[p, c] for c in range(C)) <= supply[p], f"Supply_Constraint_{p}"

# 2. Demand satisfaction constraint for each city
for c in range(C):
    problem += pulp.lpSum(x[p, c] for p in range(P)) == demand[c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')