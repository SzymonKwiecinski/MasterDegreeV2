import pulp

# Parsing the input data
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}
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
reg_quant = [pulp.LpVariable(f"reg_quant_{n}", lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f"over_quant_{n}", lowBound=0) for n in range(N)]
store = [pulp.LpVariable(f"store_{n}", lowBound=0) for n in range(N+1)]

# Objective function
problem += pulp.lpSum([
    reg_quant[n] * cost_regular +
    over_quant[n] * cost_overtime +
    store[n+1] * store_cost for n in range(N)
])

# Constraints
for n in range(N):
    # Regular production limit
    problem += reg_quant[n] <= max_regular_amount, f"Reg_Prod_Limit_{n}"
    
    # Demand satisfaction
    problem += reg_quant[n] + over_quant[n] + store[n] == demand[n] + store[n+1], f"Demand_Satisfaction_{n}"

# Initial storage is zero
problem += store[0] == 0, "Initial_Store"

# Solve the problem
problem.solve()

# Output results
reg_quant_output = [pulp.value(reg_quant[n]) for n in range(N)]
over_quant_output = [pulp.value(over_quant[n]) for n in range(N)]

output = {
    "reg_quant": reg_quant_output,
    "over_quant": over_quant_output
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')