import pulp

# Data
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

N = len(data['demand'])

# Create the Linear Programming problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMinimize)

# Variables
reg_quant = pulp.LpVariable.dicts("reg_quant", range(N), lowBound=0, upBound=data['max_regular_amount'])
over_quant = pulp.LpVariable.dicts("over_quant", range(N), lowBound=0)
inv = pulp.LpVariable.dicts("inv", range(N), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['cost_regular'] * reg_quant[n] + data['cost_overtime'] * over_quant[n] + data['store_cost'] * inv[n] for n in range(N))

# Constraints
problem += (inv[0] == 0)  # Initial inventory is zero

for n in range(N):
    if n == 0:
        problem += (reg_quant[n] + over_quant[n] == data['demand'][n] + inv[n])  # First month balance
    else:
        problem += (reg_quant[n] + over_quant[n] + inv[n-1] == data['demand'][n] + inv[n])  # Subsequent months balance

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')