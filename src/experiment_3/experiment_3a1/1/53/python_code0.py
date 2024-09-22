import pulp
import json

# Data in JSON format
data = {'NumTerminals': 3, 'NumDestinations': 4, 
        'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], 
        'Demand': [65, 70, 50, 45], 
        'Supply': [150, 100, 100]}

# Number of sources and destinations
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']

# Cost matrix
cost_matrix = data['Cost']

# Supply and demand lists
supply = data['Supply']
demand = data['Demand']

# Create the problem
problem = pulp.LpProblem("Soybean Transportation Problem", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", 
    ((i, j) for i in range(num_terminals) for j in range(num_destinations)), 
    lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(cost_matrix[i][j] * amount[i, j] for i in range(num_terminals) for j in range(num_destinations))

# Supply constraints
for k in range(num_terminals):
    problem += pulp.lpSum(amount[k, j] for j in range(num_destinations)) <= supply[k]

# Demand constraints
for l in range(num_destinations):
    problem += pulp.lpSum(amount[i, l] for i in range(num_terminals)) >= demand[l]

# Solve the problem
problem.solve()

# Print results
distribution = [{"from": i, "to": j, "amount": amount[i, j].varValue} 
                for i in range(num_terminals) 
                for j in range(num_destinations) 
                if amount[i, j].varValue > 0]

total_cost = pulp.value(problem.objective)

output = {
    "distribution": distribution,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')