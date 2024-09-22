import json
import pulp

# Data extraction from the provided JSON format
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Parameters
num_terminals = data['NumTerminals']
num_destinations = data['NumDestinations']
cost = data['Cost']
demand = data['Demand']
supply = data['Supply']

# Define the problem
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", (range(num_terminals), range(num_destinations)), lowBound=0)

# Objective Function
problem += pulp.lpSum(cost[i][j] * amount[i][j] for i in range(num_terminals) for j in range(num_destinations)), "Total_Cost"

# Supply Constraints
for k in range(num_terminals):
    problem += pulp.lpSum(amount[k][j] for j in range(num_destinations)) <= supply[k], f"Supply_Constraint_{k}"

# Demand Constraints
for l in range(num_destinations):
    problem += pulp.lpSum(amount[i][l] for i in range(num_terminals)) >= demand[l], f"Demand_Constraint_{l}"

# Solve the problem
problem.solve()

# Output results
distribution = [{ 'from': i, 'to': j, 'amount': amount[i][j].varValue } for i in range(num_terminals) for j in range(num_destinations) if amount[i][j].varValue > 0]

# Print the objective value
print(f'Distribution of soybeans: {distribution}')
print(f'Total Transportation Cost: {pulp.value(problem.objective)}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')