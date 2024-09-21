import pulp

# Data input
data = {
  'supply': [30, 25, 45],
  'demand': [40, 60],
  'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

P = len(supply)  # Number of power plants
C = len(demand)  # Number of cities

# Initialize the problem
problem = pulp.LpProblem("Minimize_Transmission_Costs", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((p, c) for p in range(P) for c in range(C)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(transmission_costs[p][c] * x[p, c] for p in range(P) for c in range(C))

# Supply constraints
for p in range(P):
    problem += pulp.lpSum(x[p, c] for c in range(C)) <= supply[p], f"Supply_Constraint_{p}"

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(x[p, c] for p in range(P)) == demand[c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')