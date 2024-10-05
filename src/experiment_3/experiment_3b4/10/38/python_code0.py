import pulp

# Data
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Number of periods
N = len(data['demand'])

# Problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
store = [pulp.LpVariable(f'store_{n}', lowBound=0) for n in range(N + 1)]

# Objective Function
problem += pulp.lpSum(
    data['cost_regular'] * reg_quant[n] +
    data['cost_overtime'] * over_quant[n] +
    data['store_cost'] * store[n + 1]
    for n in range(N)
)

# Constraints
problem += store[0] == 0  # Initial storage

for n in range(N):
    # Regular production limit
    problem += reg_quant[n] <= data['max_regular_amount']

    # Demand and storage balance
    problem += reg_quant[n] + over_quant[n] + store[n] == data['demand'][n] + store[n + 1]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')