import pulp

# Data
available = [40, 50, 80]
carbon = [3, 4, 3.5]
nickel = [1, 1.5, 1.8]
alloy_prices = [380, 400, 440]
steel_prices = [650, 600]
carbon_min = [3.6, 3.4]
nickel_max = [1.5, 1.7]

# Number of alloys and steels
A = len(available)
S = len(steel_prices)

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(A), range(S)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", range(S), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum(steel_prices[s] * y[s] for s in range(S)) - pulp.lpSum(alloy_prices[a] * x[a][s] for a in range(A) for s in range(S))
problem += profit

# Constraints
# Alloy availability
for a in range(A):
    problem += pulp.lpSum(x[a][s] for s in range(S)) <= available[a]

# Carbon content requirement
for s in range(S):
    problem += pulp.lpSum(carbon[a] * x[a][s] for a in range(A)) >= carbon_min[s] * y[s]

# Nickel content restriction
for s in range(S):
    problem += pulp.lpSum(nickel[a] * x[a][s] for a in range(A)) <= nickel_max[s] * y[s]

# Alloy 1 usage restriction
for s in range(S):
    problem += x[0][s] <= 0.4 * y[s]

# Total steel produced definition
for s in range(S):
    problem += y[s] == pulp.lpSum(x[a][s] for a in range(A))

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')