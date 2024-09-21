import pulp

# Data
supply = [30, 25, 45]  # Supply capacity of power plants
demand = [40, 60]      # Demand of cities
transmission_costs = [[14, 22], [18, 12], [10, 16]]  # Transmission costs

# Number of power plants and cities
P = len(supply)
C = len(demand)

# Create the problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(P), range(C)), lowBound=0)

# Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * x[p][c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Constraints

# Supply constraints
for p in range(P):
    problem += pulp.lpSum(x[p][c] for c in range(C)) <= supply[p], f"Supply_Capacity_Plant_{p}"

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(x[p][c] for p in range(P)) == demand[c], f"Demand_City_{c}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')