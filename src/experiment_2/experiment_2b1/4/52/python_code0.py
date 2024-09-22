import pulp
import json

# Input data
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

# Extracting data
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']
P = len(supply)  # number of power plants
C = len(demand)  # number of cities

# Create the LP problem
problem = pulp.LpProblem("Electricity_Transmission_Cost_Minimization", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0)

# Objective Function
problem += pulp.lpSum(transmission_costs[p][c] * send[p, c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Constraints
# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p, c] for c in range(C)) <= supply[p], f"Supply_Constraint_P{p}"

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p, c] for p in range(P)) >= demand[c], f"Demand_Constraint_C{c}"

# Solve the LP problem
problem.solve()

# Extract the results
send_results = [[pulp.value(send[p, c]) for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

# Output results
output = {
    "send": send_results,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')