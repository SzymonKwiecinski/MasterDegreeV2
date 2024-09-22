import pulp
import json

# Given data in JSON format
data = {'NumTerminals': 3, 'NumDestinations': 4, 
        'Cost': [[34, 49, 17, 26], 
                 [52, 64, 23, 14], 
                 [20, 28, 12, 17]], 
        'Demand': [65, 70, 50, 45], 
        'Supply': [150, 100, 100]}

# Define the problem
problem = pulp.LpProblem("Soybean_Transportation", pulp.LpMinimize)

# Create decision variables
routes = [(i, j) for i in range(data['NumTerminals']) for j in range(data['NumDestinations'])]
amount = pulp.LpVariable.dicts("amount", routes, lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['Cost'][i][j] * amount[(i, j)] for i in range(data['NumTerminals']) for j in range(data['NumDestinations'])), "Total Transportation Cost"

# Supply constraints
for i in range(data['NumTerminals']):
    problem += pulp.lpSum(amount[(i, j)] for j in range(data['NumDestinations'])) <= data['Supply'][i], f"Supply_Constraint_{i}"

# Demand constraints
for j in range(data['NumDestinations']):
    problem += pulp.lpSum(amount[(i, j)] for i in range(data['NumTerminals'])) >= data['Demand'][j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare the result
distribution = [{"from": i, "to": j, "amount": amount[(i, j)].varValue} for i, j in routes if amount[(i, j)].varValue > 0]
total_cost = pulp.value(problem.objective)

# Output result
result = {
    "distribution": distribution,
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')