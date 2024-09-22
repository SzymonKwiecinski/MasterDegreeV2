import pulp
import json

# Data initialization
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

# Model
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", 
    ((i, j) for i in range(data['NumTerminals'])
     for j in range(data['NumDestinations'])), 
    lowBound=0)  # Non-negativity constraints

# Objective Function
problem += pulp.lpSum(data['Cost'][i][j] * amount[(i, j)] 
                       for i in range(data['NumTerminals']) 
                       for j in range(data['NumDestinations'])), "Total_Transportation_Cost"

# Supply Constraints
for k in range(data['NumTerminals']):
    problem += pulp.lpSum(amount[(k, j)] for j in range(data['NumDestinations'])) <= data['Supply'][k], f"Supply_Constraint_{k}"

# Demand Constraints
for l in range(data['NumDestinations']):
    problem += pulp.lpSum(amount[(i, l)] for i in range(data['NumTerminals'])) >= data['Demand'][l], f"Demand_Constraint_{l}"

# Solve the problem
problem.solve()

# Output
distribution = []
for (i, j) in amount:
    if amount[(i, j)].varValue > 0:
        distribution.append({
            "from": i,
            "to": j,
            "amount": amount[(i, j)].varValue
        })

output = {
    "distribution": distribution,
    "total_cost": pulp.value(problem.objective)
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print the distribution
print(json.dumps(output, indent=4))