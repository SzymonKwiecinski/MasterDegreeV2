import pulp

# Data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Number of periods
N = len(data['price'])

# Linear Programming Problem
problem = pulp.LpProblem("Warehouse Management", pulp.LpMaximize)

# Decision variables
buyquantity = [pulp.LpVariable(f'buyquantity_{n}', lowBound=0) for n in range(N)]
sellquantity = [pulp.LpVariable(f'sellquantity_{n}', lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f'stock_{n}', lowBound=0) for n in range(N)]

# Objective function
profit = pulp.lpSum([
    data['price'][n] * sellquantity[n] - data['cost'][n] * buyquantity[n] - data['holding_cost'] * stock[n]
    for n in range(N)
])
problem += profit

# Constraints
# Stock balance for the first period
problem += stock[0] == buyquantity[0] - sellquantity[0], f"Stock_Balance_1"

# Stock balance for subsequent periods
for n in range(1, N):
    problem += stock[n] == stock[n-1] + buyquantity[n] - sellquantity[n], f"Stock_Balance_{n+1}"

# Stock should not exceed capacity
for n in range(N):
    problem += stock[n] <= data['capacity'], f"Capacity_Constraint_{n+1}"

# Stock should be zero at the end of the last period
problem += stock[N-1] == 0, "Final_Stock_Zero"

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')