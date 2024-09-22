import pulp

# Data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

N = len(data['price'])  # Number of periods

# Create a Linear Programming problem
problem = pulp.LpProblem("Warehouse_Operation", pulp.LpMaximize)

# Define decision variables
buyquantity = [pulp.LpVariable(f"buyquantity_{n}", lowBound=0) for n in range(N)]
sellquantity = [pulp.LpVariable(f"sellquantity_{n}", lowBound=0) for n in range(N)]
stock = [pulp.LpVariable(f"stock_{n}", lowBound=0) for n in range(N + 1)]

# Objective Function
profit = pulp.lpSum(data['price'][n] * sellquantity[n] -
                    data['cost'][n] * buyquantity[n] -
                    data['holding_cost'] * stock[n] for n in range(N))
problem += profit

# Constraints
problem += stock[0] == 0  # Initial stock
problem += stock[N] == 0  # Final stock

for n in range(1, N + 1):
    problem += stock[n] == stock[n - 1] + buyquantity[n - 1] - sellquantity[n - 1]
    problem += stock[n] <= data['capacity']

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')