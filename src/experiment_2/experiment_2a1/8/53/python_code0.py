import pulp
import json

data = {'NumTerminals': 3, 'NumDestinations': 4, 'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], 'Demand': [65, 70, 50, 45], 'Supply': [150, 100, 100]}

num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
cost = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Create the LP problem
problem = pulp.LpProblem("Soybean_Transportation_Problem", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", ((i, j) for i in range(num_terminals) for j in range(num_destinations)), lowBound=0)

# Objective function
problem += pulp.lpSum(cost[i][j] * amount[(i, j)] for i in range(num_terminals) for j in range(num_destinations))

# Supply constraints
for i in range(num_terminals):
    problem += pulp.lpSum(amount[(i, j)] for j in range(num_destinations)) <= supply[i]

# Demand constraints
for j in range(num_destinations):
    problem += pulp.lpSum(amount[(i, j)] for i in range(num_terminals)) >= demand[j]

# Solve the problem
problem.solve()

# Prepare results
distribution = [{"from": i, "to": j, "amount": amount[(i, j)].varValue} for i in range(num_terminals) for j in range(num_destinations) if amount[(i, j)].varValue > 0]

total_cost = pulp.value(problem.objective)

result = {
    "distribution": distribution,
    "total_cost": total_cost
}

# Print objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')