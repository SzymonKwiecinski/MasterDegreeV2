import pulp

# Data
supply = [30, 25, 45]  # Supply capacities for each power plant
demand = [40, 60]      # Demand for each city
transmission_costs = [[14, 22], [18, 12], [10, 16]]  # Transmission costs from power plants to cities

# Parameters
P = len(supply)         # Number of power plants
C = len(demand)         # Number of cities

# Create the problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(P), range(C)), lowBound=0)  # Amount of electricity transmitted

# Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * x[p][c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Constraints
# 1. Supply constraints for each power plant
for p in range(P):
    problem += pulp.lpSum(x[p][c] for c in range(C)) <= supply[p], f"Supply_Constraint_{p}"

# 2. Demand constraints for each city
for c in range(C):
    problem += pulp.lpSum(x[p][c] for p in range(P)) == demand[c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')