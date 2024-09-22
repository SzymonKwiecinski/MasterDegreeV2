import pulp
import json

# Data
data = """{'M': 4, 'N': 2, 'A': [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]], 'B': [2.0, 2.0, 3.0, 5.0]}"""
data = json.loads(data)

M = data['M']
N = data['N']
A = data['A']
B = data['B']

# Create the problem
problem = pulp.LpProblem("Chebychev_Center", pulp.LpMaximize)

# Decision Variables
y = pulp.LpVariable.dicts("y", range(N), lowBound=None)
r = pulp.LpVariable("r", lowBound=0)

# Objective Function
problem += r

# Constraints
for i in range(M):
    problem += (pulp.lpSum(A[i][j] * y[j] for j in range(N)) - B[i] + r <= 0)
    problem += (-B[i] + pulp.lpSum(A[i][j] * y[j] for j in range(N)) + r <= 0)

# Solve the problem
problem.solve()

# Output the results
center = [y[j].varValue for j in range(N)]
radius = r.varValue

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Center: {center}, Radius: {radius}')