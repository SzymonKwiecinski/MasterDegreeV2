import pulp
import json

# Input data
data = {'supply': [30, 25, 45], 'demand': [40, 60], 'transmission_costs': [[14, 22], [18, 12], [10, 16]]}

# Problem setup
P = len(data['supply'])  # number of power plants
C = len(data['demand'])   # number of cities

problem = pulp.LpProblem("Electricity_Transmission_Cost_Minimization", pulp.LpMinimize)

# Decision Variables
send = pulp.LpVariable.dicts("send", (range(P), range(C)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['transmission_costs'][p][c] * send[p][c] for p in range(P) for c in range(C)), "Total_Transmission_Cost"

# Supply Constraints
for p in range(P):
    problem += pulp.lpSum(send[p][c] for c in range(C)) <= data['supply'][p], f"Supply_Constraint_Power_Plant_{p}"

# Demand Constraints
for c in range(C):
    problem += pulp.lpSum(send[p][c] for p in range(P)) >= data['demand'][c], f"Demand_Constraint_City_{c}"

# Solve Problem
problem.solve()

# Output the results
send_amounts = [[send[p][c].varValue for c in range(C)] for p in range(P)]
total_cost = pulp.value(problem.objective)

output = {
    "send": send_amounts,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')