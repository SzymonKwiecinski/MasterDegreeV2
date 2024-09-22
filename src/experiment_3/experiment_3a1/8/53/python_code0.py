import pulp
import json

# Given data
data = {'NumTerminals': 3, 'NumDestinations': 4, 
        'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], 
        'Demand': [65, 70, 50, 45], 
        'Supply': [150, 100, 100]}

# Define sets
A = [(k, l) for k in range(data['NumTerminals']) for l in range(data['NumDestinations'])]
k = range(data['NumTerminals'])
l = range(data['NumDestinations'])

# Define parameters
C = {(i, j): data['Cost'][i][j] for i in range(data['NumTerminals']) for j in range(data['NumDestinations'])}
supply = {i: data['Supply'][i] for i in range(data['NumTerminals'])}
demand = {j: data['Demand'][j] for j in range(data['NumDestinations'])}

# Create the problem
problem = pulp.LpProblem("Soybean_Transportation", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", A, lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(C[i, j] * amount[i, j] for (i, j) in A)

# Supply constraints
for k_i in k:
    problem += pulp.lpSum(amount[k_i, j] for j in range(data['NumDestinations'])) <= supply[k_i]

# Demand constraints
for l_j in l:
    problem += pulp.lpSum(amount[i, l_j] for i in range(data['NumTerminals'])) >= demand[l_j]

# Solve the problem
problem.solve()

# Output results
distribution = [{"from": i, "to": j, "amount": amount[i, j].varValue} for (i, j) in A]
total_cost = pulp.value(problem.objective)

print(f'Distribution: {distribution}')
print(f'Total transportation cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')