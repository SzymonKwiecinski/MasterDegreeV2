import pulp

# Data
data = {
    'supply': [30, 25, 45], 
    'demand': [40, 60], 
    'transmission_costs': [[14, 22], [18, 12], [10, 16]]
}

# Parameters
P = len(data['supply'])  # Number of power plants
C = len(data['demand'])   # Number of cities
supply = data['supply']   # Capacity of power plants
demand = data['demand']    # Demand of cities
transmission_costs = data['transmission_costs']  # Transmission costs

# Create the problem
problem = pulp.LpProblem("Electricity_Distribution", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0)

# Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * send[(p, c)] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[(p, c)] for c in range(C)) <= supply[p], f"Supply_Constraint_{p}"

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[(p, c)] for p in range(P)) >= demand[c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Output results
send_results = {f"send_{p}_{c}": send[(p, c)].varValue for p in range(P) for c in range(C)}
total_cost = pulp.value(problem.objective)

print(send_results)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')