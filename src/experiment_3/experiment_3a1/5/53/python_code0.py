import pulp
import json

# Define the problem
problem = pulp.LpProblem("Soybean_Distribution", pulp.LpMinimize)

# Data from JSON
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
A = [(i, j) for i in K for j in L]  # Routes from terminal to destination

# Parameters
C = data['Cost']  # Transportation costs
supply = data['Supply']
demand = data['Demand']

# Decision Variables
amount = pulp.LpVariable.dicts("amount", A, lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(C[i][j] * amount[(i, j)] for i in K for j in L), "Total_Transportation_Cost"

# Supply Constraints
for k in K:
    problem += pulp.lpSum(amount[(k, j)] for j in L) <= supply[k], f"Supply_Constraint_{k}"

# Demand Constraints
for l in L:
    problem += pulp.lpSum(amount[(i, l)] for i in K) == demand[l], f"Demand_Constraint_{l}"

# Solve the problem
problem.solve()

# Output the results
distribution = [{"from": i, "to": j, "amount": amount[(i, j)].varValue} for (i, j) in A]
total_cost = pulp.value(problem.objective)

output = {
    "distribution": distribution,
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')