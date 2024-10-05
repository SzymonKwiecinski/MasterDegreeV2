import pulp

# Data 
data = {'capacity': 10, 'holding_cost': 2, 'price': [1, 2, 100], 'cost': [100, 1, 100]}
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)

# Problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"x_{n}", lowBound=0, cat='Continuous') for n in range(N)]
y = [pulp.LpVariable(f"y_{n}", lowBound=0, cat='Continuous') for n in range(N)]
s = [pulp.LpVariable(f"s_{n}", lowBound=0, upBound=capacity, cat='Continuous') for n in range(N)]

# Objective Function
problem += pulp.lpSum(price[n] * y[n] - cost[n] * x[n] - holding_cost * s[n] for n in range(N))

# Constraints
# Flow balance constraint
for n in range(N):
    if n == 0:
        problem += x[n] - y[n] == s[n], f"FlowBalance_{n}"
    else:
        problem += s[n-1] + x[n] - y[n] == s[n], f"FlowBalance_{n}"

# Initial and final stock conditions
problem += s[0] == 0, "InitialStockCondition"
problem += s[N-1] == 0, "FinalStockCondition"

# Solve
problem.solve()

# Objective value
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")