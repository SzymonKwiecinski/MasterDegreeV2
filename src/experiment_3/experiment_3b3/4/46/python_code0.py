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

# Number of alloys and steel types
A = len(data['available'])
S = len(data['steel_prices'])

# Problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

# Decision Variables
alloy_amount = pulp.LpVariable.dicts("alloy_amount", ((a, s) for a in range(A) for s in range(S)), lowBound=0, cat='Continuous')
total_steel = pulp.LpVariable.dicts("total_steel", (s for s in range(S)), lowBound=0, cat='Continuous')

# Objective Function
profit = (
    pulp.lpSum(data['steel_prices'][s] * total_steel[s] for s in range(S)) -
    pulp.lpSum(data['alloy_prices'][a] * alloy_amount[a, s] for a in range(A) for s in range(S))
)
problem += profit

# Constraints

# 1. Alloy availability
for a in range(A):
    problem += pulp.lpSum(alloy_amount[a, s] for s in range(S)) <= data['available'][a], f"Alloy_availability_{a}"

# 2. Carbon requirement
for s in range(S):
    problem += (
        pulp.lpSum(alloy_amount[a, s] * data['carbon'][a] for a in range(A)) >= data['carbon_min'][s] * total_steel[s],
        f"Carbon_requirement_{s}"
    )

# 3. Nickel limit
for s in range(S):
    problem += (
        pulp.lpSum(alloy_amount[a, s] * data['nickel'][a] for a in range(A)) <= data['nickel_max'][s] * total_steel[s],
        f"Nickel_limit_{s}"
    )

# 4. Alloy 1 restriction
problem += (
    pulp.lpSum(alloy_amount[0, s] for s in range(S)) <= 0.4 * pulp.lpSum(total_steel[s] for s in range(S)),
    "Alloy_1_restriction"
)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')