import pulp
import json

# Data
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Sets
K = range(data['NumTerminals'])  # Terminal cities
L = range(data['NumDestinations'])  # Destination cities
A = [(k, l) for k in K for l in L]  # All routes

# Parameters
C = {(k, l): data['Cost'][k][l] for k in K for l in L}  # Cost matrix
supply = {k: data['Supply'][k] for k in K}  # Supply
demand = {l: data['Demand'][l] for l in L}  # Demand

# Problem definition
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", (K, L), lowBound=0)  # amount[k][l]

# Objective Function
problem += pulp.lpSum(C[k, l] * amount[k][l] for k in K for l in L), "Total_Cost"

# Supply Constraints
for k in K:
    problem += pulp.lpSum(amount[k][l] for l in L) <= supply[k], f"Supply_Constraint_{k}"

# Demand Constraints
for l in L:
    problem += pulp.lpSum(amount[k][l] for k in K) >= demand[l], f"Demand_Constraint_{l}"

# Solve the problem
problem.solve()

# Prepare output
distribution = [{"from": k, "to": l, "amount": amount[k][l].varValue} for k in K for l in L]
total_cost = pulp.value(problem.objective)

output = {
    "distribution": distribution,
    "total_cost": total_cost
}

# Print the objective value 
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')