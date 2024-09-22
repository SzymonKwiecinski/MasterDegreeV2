import pulp

# Data
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

A = len(data['available'])
S = len(data['steel_prices'])

# Define the LP problem
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((a, s) for a in range(A) for s in range(S)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", (s for s in range(S)), lowBound=0, cat='Continuous')

# Objective Function
profit = (
    pulp.lpSum(data['steel_prices'][s] * y[s] for s in range(S)) 
    - pulp.lpSum(data['alloy_prices'][a] * x[a, s] for a in range(A) for s in range(S))
)
problem += profit

# Constraints

# 1. Alloy availability constraints
for a in range(A):
    problem += pulp.lpSum(x[a, s] for s in range(S)) <= data['available'][a]

# 2. Carbon content constraints
for s in range(S):
    problem += pulp.lpSum((data['carbon'][a] / 100) * x[a, s] for a in range(A)) >= data['carbon_min'][s] * y[s]

# 3. Nickel content constraints
for s in range(S):
    problem += pulp.lpSum((data['nickel'][a] / 100) * x[a, s] for a in range(A)) <= data['nickel_max'][s] * y[s]

# 4. Maximum limit on alloy 1 usage
problem += pulp.lpSum(x[0, s] for s in range(S)) <= 0.4 * pulp.lpSum(y[s] for s in range(S))

# Solve the problem
problem.solve()

# Print Objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')