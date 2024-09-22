import pulp

# Data parsed from JSON format
available = [40, 50, 80]
carbon = [3, 4, 3.5]
nickel = [1, 1.5, 1.8]
alloy_prices = [380, 400, 440]
steel_prices = [650, 600]
carbon_min = [3.6, 3.4]
nickel_max = [1.5, 1.7]

# Sets
A = range(len(available))  # Set of alloys
S = range(len(steel_prices))  # Set of steel types

# Problem
problem = pulp.LpProblem("Steel_Production_Problem", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((a, s) for a in A for s in S), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", (s for s in S), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(steel_prices[s] * y[s] for s in S) - pulp.lpSum(alloy_prices[a] * x[(a, s)] for a in A for s in S)

# Constraints

# Material Balance
for s in S:
    problem += y[s] == pulp.lpSum(x[(a, s)] for a in A)

# Carbon Requirement
for s in S:
    problem += pulp.lpSum(carbon[a] * x[(a, s)] for a in A) >= carbon_min[s] * y[s]

# Nickel Allowance
for s in S:
    problem += pulp.lpSum(nickel[a] * x[(a, s)] for a in A) <= nickel_max[s] * y[s]

# Alloy Availability
for a in A:
    problem += pulp.lpSum(x[(a, s)] for s in S) <= available[a]

# Alloy 1 Constraint
for s in S:
    problem += x[(0, s)] <= 0.4 * y[s]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')