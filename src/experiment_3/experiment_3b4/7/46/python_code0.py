import pulp

# Data from the provided JSON
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7]
}

# Parameters
A = 3  # Number of alloys
S = 2  # Number of steel types

# Decision Variables
x = pulp.LpVariable.dicts("x", ((a, s) for a in range(A) for s in range(S)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", (s for s in range(S)), lowBound=0, cat='Continuous')

# Problem
problem = pulp.LpProblem("Steel_Production_Profit_Maximization", pulp.LpMaximize)

# Objective Function
total_profit = (
    pulp.lpSum(data['steel_prices'][s] * y[s] for s in range(S)) - 
    pulp.lpSum(data['alloy_prices'][a] * x[(a, s)] for a in range(A) for s in range(S))
)
problem += total_profit

# Constraints

# Alloy Availability
for a in range(A):
    problem += pulp.lpSum(x[(a, s)] for s in range(S)) <= data['available'][a], f"Alloy_Availability_{a}"

# Steel Composition
for s in range(S):
    problem += y[s] == pulp.lpSum(x[(a, s)] for a in range(A)), f"Steel_Composition_{s}"

# Carbon Content Requirement
for s in range(S):
    problem += pulp.lpSum(data['carbon'][a] * x[(a, s)] for a in range(A)) >= data['carbon_min'][s] * y[s], f"Carbon_Content_{s}"

# Nickel Content Constraint
for s in range(S):
    problem += pulp.lpSum(data['nickel'][a] * x[(a, s)] for a in range(A)) <= data['nickel_max'][s] * y[s], f"Nickel_Content_{s}"

# Alloy 1 Usage Limitation
for s in range(S):
    problem += x[(0, s)] <= 0.40 * y[s], f"Alloy_1_Usage_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')