import pulp

# Data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

NumProducts = data['NumProducts']
NumMachines = data['NumMachines']
ProduceTime = data['ProduceTime']
AvailableTime = data['AvailableTime']
Profit = data['Profit']

# Problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"x_{k}", lowBound=0, cat='Continuous') for k in range(NumProducts)]

# Objective Function
problem += pulp.lpSum([Profit[k] * x[k] for k in range(NumProducts)]), "Total_Profit"

# Constraints
# Production time constraints for each machine
for m in range(NumMachines):
    problem += pulp.lpSum([ProduceTime[k][m] * x[k] for k in range(NumProducts)]) <= AvailableTime[m], f"Machine_{m}_Time"

# Solve the problem
problem.solve()

# Results
print(f"Status: {pulp.LpStatus[problem.status]}")
for k in range(NumProducts):
    print(f"Product {k + 1}: {x[k].varValue} units")
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")