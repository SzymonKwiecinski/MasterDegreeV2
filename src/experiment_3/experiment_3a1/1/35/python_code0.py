import pulp

# Data from the provided JSON-like structure
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Parameters
C = data['capacity']           # Capacity of the warehouse
h = data['holding_cost']       # Holding cost per unit
p = data['price']              # Selling price per period
c = data['cost']               # Purchase cost per period
N = len(p)                     # Number of periods

# Create the Linear Program
problem = pulp.LpProblem("Warehouse_Operations", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("Buy", range(1, N + 1), lowBound=0)  # Buying amounts
y = pulp.LpVariable.dicts("Sell", range(1, N + 1), lowBound=0) # Selling amounts
s = pulp.LpVariable.dicts("Stock", range(1, N + 1), lowBound=0) # Stock at the end of each period

# Objective Function
problem += pulp.lpSum(p[n - 1] * y[n] - c[n - 1] * x[n] - h * s[n] for n in range(1, N + 1))

# Constraints
s[1] = pulp.LpVariable("InitialStock", lowBound=0)  # Initial stock at period 1
problem += s[1] == 0  # The warehouse starts empty

for n in range(1, N + 1):
    if n > 1:
        problem += s[n] == s[n - 1] + x[n] - y[n]

    problem += s[n] <= C  # Stock should not exceed capacity
    if n == N:
        problem += s[n] == 0  # Final stock must be zero

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')