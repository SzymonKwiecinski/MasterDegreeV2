import pulp
import json

# Input data
data = json.loads("{'available': [40, 50, 80], 'carbon': [3, 4, 3.5], 'nickel': [1, 1.5, 1.8], 'alloy_prices': [380, 400, 440], 'steel_prices': [650, 600], 'carbon_min': [3.6, 3.4], 'nickel_max': [1.5, 1.7]}")

# Parameters
A = len(data['available'])  # Number of alloys
S = len(data['steel_prices'])  # Number of steel types

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(A), range(S)), lowBound=0)  # Amount of alloy a in steel s
y = pulp.LpVariable.dicts("y", range(S), lowBound=0)  # Amount of steel s

# Objective function
profit = pulp.lpSum(data['steel_prices'][s] * y[s] for s in range(S)) - \
         pulp.lpSum(data['alloy_prices'][a] * x[a][s] for a in range(A) for s in range(S))
problem += profit

# Constraints
# Alloy Availability
for a in range(A):
    problem += pulp.lpSum(x[a][s] for s in range(S)) <= data['available'][a]

# Carbon Percentage
for s in range(S):
    problem += (pulp.lpSum(data['carbon'][a] * x[a][s] for a in range(A)) / y[s]) >= data['carbon_min'][s]

# Nickel Percentage
for s in range(S):
    problem += (pulp.lpSum(data['nickel'][a] * x[a][s] for a in range(A)) / y[s]) <= data['nickel_max'][s]

# Proportion of Alloy 1
for s in range(S):
    problem += x[0][s] <= 0.4 * y[s]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')