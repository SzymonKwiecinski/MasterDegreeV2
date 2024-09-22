import pulp
import json

# Input data
data = {'NumTerminals': 3, 'NumDestinations': 4, 'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], 'Demand': [65, 70, 50, 45], 'Supply': [150, 100, 100]}

# Define the problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Define decision variables
amount = pulp.LpVariable.dicts("amount", 
                                [(i, j) for i in range(data['NumTerminals']) for j in range(data['NumDestinations'])], 
                                lowBound=0, 
                                cat='Continuous')

# Objective function: Minimize the total cost
problem += pulp.lpSum(data['Cost'][i][j] * amount[(i, j)] for i in range(data['NumTerminals']) for j in range(data['NumDestinations'])), "Total_Transportation_Cost"

# Supply constraints
for i in range(data['NumTerminals']):
    problem += pulp.lpSum(amount[(i, j)] for j in range(data['NumDestinations'])) <= data['Supply'][i], f"Supply_Constraint_terminal_{i}"

# Demand constraints
for j in range(data['NumDestinations']):
    problem += pulp.lpSum(amount[(i, j)] for i in range(data['NumTerminals'])) >= data['Demand'][j], f"Demand_Constraint_destination_{j}"

# Solve the problem
problem.solve()

# Prepare the output
distribution = []
for i in range(data['NumTerminals']):
    for j in range(data['NumDestinations']):
        if amount[(i, j)].varValue > 0:
            distribution.append({"from": i, "to": j, "amount": amount[(i, j)].varValue})

total_cost = pulp.value(problem.objective)

# Print the output
output = {
    "distribution": distribution,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')