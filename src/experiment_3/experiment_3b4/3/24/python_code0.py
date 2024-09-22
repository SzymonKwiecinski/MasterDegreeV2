import pulp

# Data
data = {
    'n_mines': 4,
    'n_maxwork': 3,
    'royalty': [5000000.0, 4000000.0, 4000000.0, 5000000.0],
    'limit': [2000000.0, 2500000.0, 1300000.0, 3000000.0],
    'quality': [1.0, 0.7, 1.5, 0.5],
    'requiredquality': [0.9, 0.8, 1.2, 0.6, 1.0],
    'price': 10,
    'discount': 0.1
}

# Sets
K = range(data['n_mines'])
I = range(len(data['requiredquality']))

# Create the problem
problem = pulp.LpProblem("Mining_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
isoperated = pulp.LpVariable.dicts("IsOperated", ((k, i) for k in K for i in I), cat='Binary')
amount = pulp.LpVariable.dicts("Amount", ((k, i) for k in K for i in I), lowBound=0)

# Objective Function
problem += pulp.lpSum(
    pulp.lpSum(
        1 / (1 + data['discount'])**i * (
            data['price'] * pulp.lpSum(amount[k, i] for k in K) -
            pulp.lpSum(data['royalty'][k] * isoperated[k, i] for k in K)
        )
    ) for i in I
)

# Constraints

# Constraint (1): Maximum number of mines that can operate in any year
for i in I:
    problem += pulp.lpSum(isoperated[k, i] for k in K) <= data['n_maxwork'], f"MaxMines_Year_{i}"

# Constraint (2): Ore extraction limits
for i in I:
    for k in K:
        problem += amount[k, i] <= data['limit'][k] * isoperated[k, i], f"Limit_Mine_{k}_Year_{i}"

# Constraint (3): Quality requirements
for i in I:
    problem += pulp.lpSum(amount[k, i] * data['quality'][k] for k in K) == \
               data['requiredquality'][i] * pulp.lpSum(amount[k, i] for k in K), f"Quality_Year_{i}"

# Constraint (4): Once closed, cannot reopen
for i in range(len(I) - 1):
    for k in K:
        problem += isoperated[k, i] >= isoperated[k, i + 1], f"NoReopen_Mine_{k}_Year_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')