import pulp
import json

# Input data
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

# Extract inputs
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Number of power plants (P) and cities (C)
P = len(supply)
C = len(demand)

# Create the LP problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

# Decision variables: send_p_c is how much plant p sends to city c
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0, cat='Continuous')

# Objective function: minimize total transmission cost
problem += pulp.lpSum(transmission_costs[p][c] * send[p][c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= supply[p], f"Supply_Constraint_P{p}"

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) >= demand[c], f"Demand_Constraint_C{c}"

# Solve the problem
problem.solve()

# Prepare output
send_solution = [[pulp.value(send[p][c]) for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

# Output format
output = {
    "send": send_solution,
    "total_cost": total_cost
}

# Print the result
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')