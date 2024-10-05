import pulp

# Data
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

# Model
problem = pulp.LpProblem("Production_Optimization", pulp.LpMinimize)

# Decision Variables
reg_quant = pulp.LpVariable.dicts("reg_quant", range(N), lowBound=0)
over_quant = pulp.LpVariable.dicts("over_quant", range(N), lowBound=0)
inv = pulp.LpVariable.dicts("inv", range(N), lowBound=0)

# Objective Function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inv[n] for n in range(N))

# Constraints
for n in range(N):
    problem += (reg_quant[n] + over_quant[n] + (inv[n-1] if n > 0 else 0) == demand[n] + inv[n])

for n in range(N):
    problem += reg_quant[n] <= max_regular_amount

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')