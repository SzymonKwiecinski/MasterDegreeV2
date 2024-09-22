import pulp

# Data
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Problem
problem = pulp.LpProblem("Production_Plan", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0) for i in range(T)]
I = [pulp.LpVariable(f"I_{i}", lowBound=0) for i in range(T)]

# Objective Function
problem += pulp.lpSum(storage_cost * I[i] + switch_cost * (pulp.lpSum(x[i+1] - x[i] for i in range(T-1))) for i in range(T))

# Constraints
problem += (I[0] == x[0] - deliver[0])
for i in range(1, T):
    problem += (I[i] == I[i-1] + x[i] - deliver[i])

problem += (I[T-1] == 0)

# Solve
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')