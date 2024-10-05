import pulp

# Data Setup
data = {
    'NumTerminals': 3,
    'NumDestinations': 4,
    'Cost': [
        [34, 49, 17, 26],
        [52, 64, 23, 14],
        [20, 28, 12, 17]
    ],
    'Demand': [65, 70, 50, 45],
    'Supply': [150, 100, 100]
}

NumTerminals = data['NumTerminals']
NumDestinations = data['NumDestinations']
Cost = data['Cost']
Demand = data['Demand']
Supply = data['Supply']

# Problem Creation
problem = pulp.LpProblem("Soybean_Transport", pulp.LpMinimize)

# Decision Variables: x[i][j] represents the amount shipped from terminal i to destination j
x = [[pulp.LpVariable(f"x_{i}_{j}", lowBound=0, cat='Continuous')
      for j in range(NumDestinations)] for i in range(NumTerminals)]

# Objective Function
problem += pulp.lpSum(Cost[i][j] * x[i][j] for i in range(NumTerminals) for j in range(NumDestinations))

# Supply Constraints
for i in range(NumTerminals):
    problem += pulp.lpSum(x[i][j] for j in range(NumDestinations)) <= Supply[i]

# Demand Constraints
for j in range(NumDestinations):
    problem += pulp.lpSum(x[i][j] for i in range(NumTerminals)) >= Demand[j]

# Solve the problem
problem.solve()

# Results
distribution = []
for i in range(NumTerminals):
    for j in range(NumDestinations):
        amount = x[i][j].varValue
        if amount > 0:
            distribution.append({
                "from": i,
                "to": j,
                "amount": amount
            })

result = {
    "distribution": distribution,
    "total_cost": pulp.value(problem.objective)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')