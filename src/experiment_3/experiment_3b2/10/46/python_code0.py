import pulp

# Data extracted from the provided JSON format
available = [40, 50, 80]
carbon = [3, 4, 3.5]
nickel = [1, 1.5, 1.8]
alloy_prices = [380, 400, 440]
steel_prices = [650, 600]
carbon_min = [3.6, 3.4]
nickel_max = [1.5, 1.7]

A = len(available)  # Number of alloys
S = len(steel_prices)  # Number of steel types

# Create the Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(A), range(S)), lowBound=0)

# Objective function
profit = pulp.lpSum(steel_prices[s] * pulp.lpSum(x[a][s] for a in range(A)) for s in range(S)) - \
                   pulp.lpSum(alloy_prices[a] * pulp.lpSum(x[a][s] for s in range(S)) for a in range(A))

problem += profit, "Objective"

# Constraints
# available constraints
for a in range(A):
    problem += pulp.lpSum(x[a][s] for s in range(S)) <= available[a], f"Available_Alloy_{a+1}"

# carbon constraints
for s in range(S):
    problem += (pulp.lpSum(carbon[a] * x[a][s] for a in range(A)) /
                 pulp.lpSum(x[a][s] for a in range(A))) >= carbon_min[s], f"Carbon_Min_{s+1}"

# nickel constraints
for s in range(S):
    problem += (pulp.lpSum(nickel[a] * x[a][s] for a in range(A)) /
                 pulp.lpSum(x[a][s] for a in range(A))) <= nickel_max[s], f"Nickel_Max_{s+1}"

# x1,s constraints
for s in range(S):
    problem += x[0][s] <= 0.4 * pulp.lpSum(x[a][s] for a in range(A)), f"X1_Constraint_{s+1}"

# total steel constraints
for s in range(S):
    problem += pulp.lpSum(x[a][s] for a in range(A)) == available[0], f"Total_Steel_{s+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')