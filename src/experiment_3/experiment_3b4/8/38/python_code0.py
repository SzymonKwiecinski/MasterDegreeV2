import pulp

# Data provided
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Number of periods
N = len(data['demand'])

# Create a Linear Programming problem
problem = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

# Define decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0, cat='Continuous') for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0, cat='Continuous') for n in range(N)]
store = [pulp.LpVariable(f'store_{n}', lowBound=0, cat='Continuous') for n in range(N)]

# Objective Function
total_cost = pulp.lpSum(
    data['cost_regular'] * reg_quant[n] + 
    data['cost_overtime'] * over_quant[n] +
    data['store_cost'] * store[n] 
    for n in range(N)
)

problem += total_cost

# Constraints
# Storage initial condition
problem += store[0] == 0

# Demand and production constraints
for n in range(N):
    problem += reg_quant[n] <= data['max_regular_amount']
    if n == 0:
        problem += reg_quant[n] + over_quant[n] - store[n] == data['demand'][n]
    else:
        problem += reg_quant[n] + over_quant[n] + store[n-1] - store[n] == data['demand'][n]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')