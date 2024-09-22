import pulp

# Extracting data from the JSON
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demand)

# Create LP problem
problem = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{n}', lowBound=0, cat='Continuous') for n in range(N)]
y = [pulp.LpVariable(f'y_{n}', lowBound=0, cat='Continuous') for n in range(N)]
s = [pulp.LpVariable(f's_{n}', lowBound=0, cat='Continuous') for n in range(N)]

# Objective function
problem += pulp.lpSum(cost_regular * x[n] + cost_overtime * y[n] + store_cost * s[n] for n in range(N))

# Constraints
s_prev = 0  # Initial inventory
for n in range(N):
    # Balance constraint
    problem += x[n] + y[n] + s_prev == demand[n] + s[n]
    
    # Maximum regular production constraint
    problem += x[n] <= max_regular_amount
    
    # Update previous storage for the next period
    s_prev = s[n]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')