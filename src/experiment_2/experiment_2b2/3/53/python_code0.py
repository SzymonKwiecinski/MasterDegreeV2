import pulp

# Define the data
data = {'NumTerminals': 3, 'NumDestinations': 4, 'Cost': [[34, 49, 17, 26], [52, 64, 23, 14], [20, 28, 12, 17]], 'Demand': [65, 70, 50, 45], 'Supply': [150, 100, 100]}

# Extract data
NumTerminals = data['NumTerminals']
NumDestinations = data['NumDestinations']
Cost = data['Cost']
Demand = data['Demand']
Supply = data['Supply']

# Initialize the problem
problem = pulp.LpProblem("Soybean_Transport_Problem", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("Amount", ((i, j) for i in range(NumTerminals) for j in range(NumDestinations)), lowBound=0, cat="Continuous")

# Objective function
problem += pulp.lpSum(Cost[i][j] * amount[i, j] for i in range(NumTerminals) for j in range(NumDestinations))

# Supply constraints
for i in range(NumTerminals):
    problem += pulp.lpSum(amount[i, j] for j in range(NumDestinations)) <= Supply[i], f"Supply_Constraint_{i}"

# Demand constraints
for j in range(NumDestinations):
    problem += pulp.lpSum(amount[i, j] for i in range(NumTerminals)) >= Demand[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare the result
distribution = [
    {"from": i, "to": j, "amount": amount[i, j].varValue or 0}
    for i in range(NumTerminals) for j in range(NumDestinations)
]

total_cost = pulp.value(problem.objective)

# Print the outcome
print({
    "distribution": distribution,
    "total_cost": total_cost
})

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')