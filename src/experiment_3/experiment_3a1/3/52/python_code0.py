import pulp

# Data
supply = [30, 25, 45]  # Capacity of power plants
demand = [40, 60]      # Demand of cities
transmission_costs = [[14, 22], [18, 12], [10, 16]]  # Transmission costs

# Parameters
P = len(supply)  # Number of power plants
C = len(demand)  # Number of cities

# Create the linear programming problem
problem = pulp.LpProblem("ElectricUtility", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0)

# Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * send[p][c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Constraints
# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= supply[p], f"Supply_Constraint_{p}"

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) >= demand[c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Print the results
for p in range(P):
    for c in range(C):
        print(f'Send from Power Plant {p} to City {c}: {send[p][c].varValue} million kwh')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')