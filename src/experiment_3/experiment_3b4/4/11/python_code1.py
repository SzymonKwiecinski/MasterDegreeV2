import pulp

# Input data
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
problem = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(1, T+1)]
I = [pulp.LpVariable(f"I_{i}", lowBound=0, cat='Continuous') for i in range(1, T+1)]

# Objective Function
storage_cost_term = pulp.lpSum([storage_cost * I[i] for i in range(T)])
switch_cost_term = pulp.lpSum([switch_cost * (x[i+1] - x[i]) for i in range(T-1)]) + pulp.lpSum([switch_cost * (x[i] - x[i+1]) for i in range(T-1)])  # fixed to avoid abs()
problem += storage_cost_term + switch_cost_term, "Total Cost"

# Constraints
problem += (0 + x[0] == deliver[0] + I[0])  # I_0 = 0

for i in range(1, T):
    problem += (I[i-1] + x[i] == deliver[i] + I[i])

# Solve
problem.solve()

# Print the objective value