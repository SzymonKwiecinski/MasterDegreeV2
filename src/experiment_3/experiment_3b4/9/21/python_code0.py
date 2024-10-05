import pulp

# Data from the JSON
num_machines = [4, 2, 3, 1, 1]
profit = [10, 6, 8, 4, 11, 9, 3]
time = [
    [0.5, 0.1, 0.2, 0.05, 0.0],
    [0.7, 0.2, 0.0, 0.03, 0.0],
    [0.0, 0.0, 0.8, 0.0, 0.01],
    [0.0, 0.3, 0.0, 0.07, 0.0],
    [0.3, 0.0, 0.0, 0.1, 0.05],
    [0.5, 0.0, 0.6, 0.08, 0.05]
]
down = [0, 1, 1, 1, 1]
limit = [
    [500, 600, 300, 200, 0, 500],
    [1000, 500, 600, 300, 100, 500],
    [300, 200, 0, 400, 500, 100],
    [300, 0, 0, 500, 100, 300],
    [800, 400, 500, 200, 1000, 1100],
    [200, 300, 400, 0, 300, 500],
    [100, 150, 100, 100, 0, 60]
]
store_price = 0.5
keep_quantity = 100
n_workhours = 8.0
shifts_per_month = 12  # 6 days/week * 2 shifts/day * 4 weeks

# Set definitions
K = range(len(profit))
M = range(len(num_machines))
I = range(len(limit[0]))

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
sell = pulp.LpVariable.dicts("sell", (K, I), lowBound=0, cat='Continuous')
manufacture = pulp.LpVariable.dicts("manufacture", (K, I), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (K, I), lowBound=0, upBound=100, cat='Continuous')
maintain = pulp.LpVariable.dicts("maintain", (M, I), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(
    profit[k] * sell[k][i] - store_price * storage[k][i] for k in K for i in I
)

# Constraints
# Demand constraints
for k in K:
    for i in I:
        problem += sell[k][i] <= limit[k][i]

# Production constraints
for m in M:
    for i in I:
        problem += pulp.lpSum(time[k][m] * manufacture[k][i] for k in K) <= \
                   (num_machines[m] - maintain[m][i]) * n_workhours * shifts_per_month

# Machine maintenance constraints
for m in M:
    problem += pulp.lpSum(maintain[m][i] for i in I) == down[m]

# Storage balance constraints
for k in K:
    problem += storage[k][0] == 0
    for i in range(1, len(I)):
        problem += storage[k][i] == storage[k][i-1] + manufacture[k][i] - sell[k][i]
    problem += storage[k][len(I)-1] == keep_quantity

# Non-negativity constraints are handled by the LpVariable definitions

# Solve the problem
problem.solve()

# Objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')