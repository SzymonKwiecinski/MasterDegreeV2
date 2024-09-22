import pulp

# Define data
data = {
    'available': [40, 50, 80],
    'carbon': [3, 4, 3.5],
    'nickel': [1, 1.5, 1.8],
    'alloy_prices': [380, 400, 440],
    'steel_prices': [650, 600],
    'carbon_min': [3.6, 3.4],
    'nickel_max': [1.5, 1.7],
}

# Set constants
A = 3  # Number of alloys
S = 2  # Number of types of steel

# Initialize the problem
problem = pulp.LpProblem("Steel_Production_Profit_Maximization", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((a, s) for a in range(A) for s in range(S)), lowBound=0, cat='Continuous')
total_steel = pulp.LpVariable.dicts("total_steel", (s for s in range(S)), lowBound=0, cat='Continuous')

# Objective function
problem += (
    pulp.lpSum(data['steel_prices'][s] * total_steel[s] for s in range(S)) -
    pulp.lpSum(data['alloy_prices'][a] * x[(a, s)] for a in range(A) for s in range(S))
), "Total_Profit"

# Constraints
# Alloy availability constraints
for a in range(A):
    problem += (
        pulp.lpSum(x[(a, s)] for s in range(S)) <= data['available'][a]
    ), f"Alloy_Availability_{a}"

# Carbon requirement constraints
for s in range(S):
    problem += (
        pulp.lpSum(x[(a, s)] * data['carbon'][a] for a in range(A)) >= data['carbon_min'][s] * total_steel[s]
    ), f"Carbon_Requirement_{s}"

# Nickel requirement constraints
for s in range(S):
    problem += (
        pulp.lpSum(x[(a, s)] * data['nickel'][a] for a in range(A)) <= data['nickel_max'][s] * total_steel[s]
    ), f"Nickel_Requirement_{s}"

# Alloy 1 limitation
problem += (
    pulp.lpSum(x[(0, s)] for s in range(S)) <= 0.4 * pulp.lpSum(total_steel[s] for s in range(S))
), "Alloy_1_Limitation"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')