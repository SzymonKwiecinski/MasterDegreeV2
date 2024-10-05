import pulp

# Load the data
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Number of months
N = len(demand)

# Create the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
store = [pulp.LpVariable(f'store_{n}', lowBound=0) for n in range(N)]

# Objective function
problem += (
    pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * store[n] for n in range(N))
)

# Constraints
for n in range(N):
    if n == 0:
        problem += reg_quant[n] + over_quant[n] - store[n] == demand[n], f'demand_constraint_{n}'
    else:
        problem += reg_quant[n] + over_quant[n] + store[n-1] - store[n] == demand[n], f'demand_constraint_{n}'

    problem += reg_quant[n] <= max_regular_amount, f'regular_production_constraint_{n}'

# Solve the problem
problem.solve()

# Gather results
output = {
    "reg_quant": [pulp.value(reg_quant[n]) for n in range(N)],
    "over_quant": [pulp.value(over_quant[n]) for n in range(N)],
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')