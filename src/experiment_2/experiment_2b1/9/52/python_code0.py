import pulp
import json

# Input data
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

# Create the LP problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

# Define sets
P = len(data['supply'])  # Number of power plants
C = len(data['demand'])   # Number of cities

# Decision variables: amount of electricity sent from power plant p to city c
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0)

# Objective Function: Minimize the total transmission cost
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[p][c] for p in range(P) for c in range(C))

# Constraints
# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_{p}"

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) >= data['demand'][c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Extract the results
send_results = [[pulp.value(send[p][c]) for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

# Output results
output = {
    "send": send_results,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')