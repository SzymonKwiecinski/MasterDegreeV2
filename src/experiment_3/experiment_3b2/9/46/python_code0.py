import pulp

# Data from JSON format
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

# Number of alloys and steels
A = len(data['available'])       # Number of alloys
S = len(data['steel_prices'])    # Number of steel types

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((a, s) for a in range(A) for s in range(S)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", (s for s in range(S)), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum(data['steel_prices'][s] * y[s] for s in range(S)) - \
         pulp.lpSum(data['alloy_prices'][a] * x[a, s] for a in range(A) for s in range(S))
problem += profit

# Constraints
# Available alloy constraints
for a in range(A):
    problem += pulp.lpSum(x[a, s] for s in range(S)) <= data['available'][a]

# Carbon minimum constraints
for s in range(S):
    problem += pulp.lpSum((data['carbon'][a] / 100) * x[a, s] for a in range(A)) >= data['carbon_min'][s] * y[s]

# Nickel maximum constraints
for s in range(S):
    problem += pulp.lpSum((data['nickel'][a] / 100) * x[a, s] for a in range(A)) <= data['nickel_max'][s] * y[s]

# Alloy proportion constraint
for s in range(S):
    problem += x[0, s] <= 0.4 * pulp.lpSum(x[a, s] for a in range(A))

# Production relationship constraint
for s in range(S):
    problem += y[s] == pulp.lpSum(x[a, s] for a in range(A))

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')