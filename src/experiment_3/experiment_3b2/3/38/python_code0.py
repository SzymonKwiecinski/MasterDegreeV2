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

# Create the linear programming problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision Variables
reg_quant = pulp.LpVariable.dicts("reg_quant", range(N), lowBound=0, upBound=data['max_regular_amount'])
over_quant = pulp.LpVariable.dicts("over_quant", range(N), lowBound=0)
store_quant = pulp.LpVariable.dicts("store_quant", range(N), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['cost_regular'] * reg_quant[n] + 
                       data['cost_overtime'] * over_quant[n] + 
                       data['store_cost'] * store_quant[n] for n in range(N))

# Constraints
for n in range(N):
    if n == 0:
        problem += (reg_quant[n] + over_quant[n] - store_quant[n] == data['demand'][n])
    else:
        problem += (reg_quant[n] + over_quant[n] + store_quant[n-1] - store_quant[n] == data['demand'][n])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')