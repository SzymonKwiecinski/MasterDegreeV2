import pulp

# Define the data from the JSON input
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}

# Unpack the data
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Number of months
N = len(demand)

# Initialize the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
store = [pulp.LpVariable(f'store_{n}', lowBound=0) for n in range(N + 1)]

# Objective function: Minimize the cost
problem += (
    pulp.lpSum(cost_regular * reg_quant[n] for n in range(N)) +
    pulp.lpSum(cost_overtime * over_quant[n] for n in range(N)) +
    pulp.lpSum(store_cost * store[n + 1] for n in range(N))
)

# Constraints
store[0] = 0  # Initial storage is zero

for n in range(N):
    # Demand constraint
    problem += reg_quant[n] + over_quant[n] + store[n] == demand[n] + store[n + 1]
    # Max regular production constraint
    problem += reg_quant[n] <= max_regular_amount

# Solve the problem
problem.solve()

# Extract results
reg_quant_values = [pulp.value(reg_quant[n]) for n in range(N)]
over_quant_values = [pulp.value(over_quant[n]) for n in range(N)]

# Output results in the specified format
output = {
    "reg_quant": reg_quant_values,
    "over_quant": over_quant_values
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')