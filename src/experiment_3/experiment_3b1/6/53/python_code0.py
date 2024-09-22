import pulp
import json

# Data provided in JSON format
data = json.loads('{"NumTerminals": 3, "NumDestinations": 4, "Cost": [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], "Demand": [65, 70, 50, 45], "Supply": [150, 100, 100]}')

# Sets
K = range(data['NumTerminals'])  # Terminal cities
L = range(data['NumDestinations'])  # Destination cities
A = [(k, l) for k in K for l in L]  # All routes

# Parameters
C = data['Cost']  # Transport cost
supply = data['Supply']  # Soybean supply at terminal cities
demand = data['Demand']  # Soybean demand at destination cities

# Problem Definition
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", A, lowBound=0)  # Amount of soybeans shipped

# Objective Function
problem += pulp.lpSum(C[i][j] * amount[(i, j)] for i in K for j in L), "Total_Transport_Cost"

# Supply Constraints
for k in K:
    problem += pulp.lpSum(amount[(k, j)] for j in L) <= supply[k], f"Supply_Constraint_{k}"

# Demand Constraints
for l in L:
    problem += pulp.lpSum(amount[(i, l)] for i in K) >= demand[l], f"Demand_Constraint_{l}"

# Solve the problem
problem.solve()

# Output the results
distribution = [{"from": i, "to": j, "amount": amount[(i, j)].varValue} for (i, j) in A if amount[(i, j)].varValue > 0]

print(f'{"distribution"}: {distribution}')
print(f'{"total_cost"}: {pulp.value(problem.objective)}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')