import pulp

# Input data
data = {
    "demand": [10.0, 20.0, 10.0],
    "max_regular_amount": 5.0,
    "cost_regular": 10.0,
    "cost_overtime": 12.0,
    "store_cost": 1.0
}

# Extracting the data from the JSON
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Number of months
N = len(demand)

# Create LP problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', 0, max_regular_amount, cat='Continuous') for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', 0, None, cat='Continuous') for n in range(N)]
store_quant = [pulp.LpVariable(f'store_quant_{n}', 0, None, cat='Continuous') for n in range(N)]

# Objective function: Minimize the cost
problem += pulp.lpSum(
    [cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * store_quant[n] for n in range(N)]
)

# Constraints
for n in range(N):
    # Satisfy demand
    production = reg_quant[n] + over_quant[n]
    if n == 0:
        problem += production + 0 == demand[n] + store_quant[n]
    else:
        problem += production + store_quant[n - 1] == demand[n] + store_quant[n]

# Solve the problem
problem.solve()

# Prepare output data
output = {
    "reg_quant": [pulp.value(reg_quant[n]) for n in range(N)],
    "over_quant": [pulp.value(over_quant[n]) for n in range(N)]
}

# Print results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')