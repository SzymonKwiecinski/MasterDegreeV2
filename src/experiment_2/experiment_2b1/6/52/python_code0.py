import pulp
import json

# Input data
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

# Extracting data from the input
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Define the problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

# Define the number of power plants and cities
P = len(supply)
C = len(demand)

# Create decision variables
send = pulp.LpVariable.dicts("send", ((p, c) for p in range(P) for c in range(C)), lowBound=0)

# Objective function: Minimize total transmission cost
problem += pulp.lpSum(transmission_costs[p][c] * send[p, c] for p in range(P) for c in range(C))

# Constraints: Supply constraints for each power plant
for p in range(P):
    problem += pulp.lpSum(send[p, c] for c in range(C)) <= supply[p], f"Supply_Constraint_{p}"

# Constraints: Demand constraints for each city
for c in range(C):
    problem += pulp.lpSum(send[p, c] for p in range(P)) >= demand[c], f"Demand_Constraint_{c}"

# Solve the problem
problem.solve()

# Prepare the output
send_result = [[send[p, c].varValue for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

output = {
    "send": send_result,
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# If you want to see the output, uncomment the line below
# print(json.dumps(output))