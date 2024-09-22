import pulp
import json

# Input data
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

# Problem parameters
P = len(data['supply'])
C = len(data['demand'])
supply = data['supply']
demand = data['demand']
transmission_costs = data['transmission_costs']

# Create the LP problem
problem = pulp.LpProblem("Electricity_Transmission_Cost_Minimization", pulp.LpMinimize)

# Decision variables
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(transmission_costs[p][c] * send[p][c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Constraints
# Supply constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= supply[p], f"Supply_Constraint_P{p}"

# Demand constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) >= demand[c], f"Demand_Constraint_C{c}"

# Solve the problem
problem.solve()

# Prepare the output
send_result = [[pulp.value(send[p][c]) for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

output = {
    "send": send_result,
    "total_cost": total_cost
}

# Print the output in the required format
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')