import pulp
import json

# Input data
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

P = len(data['supply'])  # Number of power plants
C = len(data['demand'])   # Number of cities

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

# Decision variables: amount of electricity sent from power plant p to city c
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0)

# Objective function: minimize the total transmission cost
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[p][c] for p in range(P) for c in range(C))

# Supply constraints: total amount sent from each power plant cannot exceed its supply
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= data['supply'][p]

# Demand constraints: total amount received by each city must meet its demand
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) == data['demand'][c]

# Solve the problem
problem.solve()

# Prepare the output
send_results = [[pulp.value(send[p][c]) for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

output = {
    "send": send_results,
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')

# Print the output to see the results
print(json.dumps(output, indent=4))