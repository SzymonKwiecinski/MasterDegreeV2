import pulp

# Data
data = {
    'T': 12, 
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
    'StorageCost': 5, 
    'SwitchCost': 10
}

T = data['T']
delivers = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Problem
problem = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Production", (i for i in range(1, T+1)), lowBound=0, cat='Continuous')
I = pulp.LpVariable.dicts("Inventory", (i for i in range(0, T)), lowBound=0, cat='Continuous')

# Objective Function
storage_cost_term = pulp.lpSum(storage_cost * I[i] for i in range(T))
switch_cost_term = pulp.lpSum(switch_cost * pulp.lpAbs(x[i+1] - x[i]) for i in range(1, T))

problem += storage_cost_term + switch_cost_term

# Constraints
problem += I[0] == 0  # Initial inventory
for i in range(1, T+1):
    problem += x[i] + (I[i-1] if i-1 in I else 0) - I[i] == delivers[i-1]  # Delivery constraints

# Solve
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')