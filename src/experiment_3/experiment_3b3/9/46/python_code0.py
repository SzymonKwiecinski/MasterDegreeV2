import pulp

# Data
available = [40, 50, 80]
carbon = [3, 4, 3.5]
nickel = [1, 1.5, 1.8]
alloy_prices = [380, 400, 440]
steel_prices = [650, 600]
carbon_min = [3.6, 3.4]
nickel_max = [1.5, 1.7]

A = len(available)  # Number of alloys
S = len(steel_prices)  # Number of steel types

# Decision Variables
x = pulp.LpVariable.dicts("x", ((a, s) for a in range(A) for s in range(S)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", (s for s in range(S)), lowBound=0, cat='Continuous')

# Problem Definition
problem = pulp.LpProblem("Steel_Production", pulp.LpMaximize)

# Objective Function
problem += (pulp.lpSum(y[s] * steel_prices[s] for s in range(S)) -
            pulp.lpSum(x[a, s] * alloy_prices[a] for a in range(A) for s in range(S)))

# Constraints
# 1. Alloy usage
for a in range(A):
    problem += pulp.lpSum(x[a, s] for s in range(S)) <= available[a]

# 2. Carbon requirement for steel
for s in range(S):
    problem += pulp.lpSum(x[a, s] * (carbon[a] / 100) for a in range(A)) >= y[s] * (carbon_min[s] / 100)

# 3. Nickel limit for steel
for s in range(S):
    problem += pulp.lpSum(x[a, s] * (nickel[a] / 100) for a in range(A)) <= y[s] * (nickel_max[s] / 100)

# 4. Limit on alloy 1 usage
problem += pulp.lpSum(x[0, s] for s in range(S)) <= 0.4 * pulp.lpSum(y[s] for s in range(S))

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')