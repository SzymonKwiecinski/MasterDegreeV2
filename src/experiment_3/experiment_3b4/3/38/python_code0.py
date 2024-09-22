import pulp

# Data from JSON
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Extracting data
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Number of months
N = len(demand)

# Initialize the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0, cat='Continuous') for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0, cat='Continuous') for n in range(N)]
invent = [pulp.LpVariable(f'invent_{n}', lowBound=0, cat='Continuous') for n in range(N+1)]

# Objective Function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * invent[n+1] for n in range(N))

# Constraints
# Initial Inventory
problem += invent[0] == 0

# Demand satisfaction and inventory constraints
for n in range(N):
    problem += reg_quant[n] + over_quant[n] + invent[n] == demand[n] + invent[n+1]

# Regular production limit
for n in range(N):
    problem += reg_quant[n] <= max_regular_amount

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')