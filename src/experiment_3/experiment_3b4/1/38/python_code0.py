import pulp

# Data from JSON
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Parameters
N = len(data['demand'])
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Problem
problem = pulp.LpProblem("ProductionPlanning", pulp.LpMinimize)

# Decision Variables
reg_quant = pulp.LpVariable.dicts("reg_quant", range(N), lowBound=0, cat='Continuous')
over_quant = pulp.LpVariable.dicts("over_quant", range(N), lowBound=0, cat='Continuous')
store = pulp.LpVariable.dicts("store", range(N), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([
    cost_regular * reg_quant[n] + 
    cost_overtime * over_quant[n] + 
    store_cost * store[n] 
    for n in range(N)
])

# Constraints
for n in range(N):
    problem += reg_quant[n] <= max_regular_amount
    if n == 0:
        problem += reg_quant[n] + over_quant[n] == demand[n] + store[n]
    else:
        problem += reg_quant[n] + over_quant[n] + store[n-1] == demand[n] + store[n]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')