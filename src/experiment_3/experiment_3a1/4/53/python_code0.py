import pulp
import json

# Given data
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
A = [(i, j) for i in K for j in L]  # All routes

# Parameters
C = {(i, j): data['Cost'][i][j] for i, j in A}  # Transportation costs
supply = {k: data['Supply'][k] for k in K}  # Supply at each terminal
demand = {l: data['Demand'][l] for l in L}  # Demand at each destination

# Decision Variables
amount = pulp.LpVariable.dicts("amount", A, lowBound=0)

# Problem Definition
problem = pulp.LpProblem("SoybeanTransportation", pulp.LpMinimize)

# Objective Function
problem += pulp.lpSum(C[i, j] * amount[i, j] for i, j in A), "TotalTransportationCost"

# Supply Constraints
for k in K:
    problem += pulp.lpSum(amount[k, j] for j in L if (k, j) in A) <= supply[k], f"SupplyConstraint_{k}"

# Demand Constraints
for l in L:
    problem += pulp.lpSum(amount[i, l] for i in K if (i, l) in A) == demand[l], f"DemandConstraint_{l}"

# Solve the problem
problem.solve()

# Output the results
distribution = [
    {"from": i, "to": j, "amount": amount[i, j].varValue}
    for i, j in A if amount[i, j].varValue > 0
]

total_cost = pulp.value(problem.objective)

output = {
    "distribution": distribution,
    "total_cost": total_cost
}

# Print Objective Value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')