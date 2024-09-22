import pulp
import json

# Input data
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

# Define the problem
problem = pulp.LpProblem("Electricity_Allocation", pulp.LpMinimize)

# Define indices
P = len(data['supply'])  # Number of power plants
C = len(data['demand'])   # Number of cities

# Variables: the amount of electricity sent from each power plant to each city
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0)

# Objective function: minimize total transmission cost
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[p][c] for p in range(P) for c in range(C))

# Constraints: supply limitations
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= data['supply'][p]

# Constraints: demand requirements
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) >= data['demand'][c]

# Solve the problem
problem.solve()

# Prepare output
output_send = [[send[p][c].varValue for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

# Output format
output = {
    "send": output_send,
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# For the final output
print(json.dumps(output))