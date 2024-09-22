import pulp
import json

# Data initialization from JSON format
data = {
    'N': 3,
    'Start': [100.0, 50.0, 200.0],
    'Limit': [1000.0, 200.0, 3000.0],
    'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]
}

# Problem definition
problem = pulp.LpProblem("Currency_Exchange_Problem", pulp.LpMaximize)

# Decision Variables
N = data['N']
x = pulp.LpVariable.dicts("x", (range(N), range(N)), lowBound=0)

# Objective Function
problem += pulp.lpSum(x[i][N-1] * data['Rate'][i][N-1] for i in range(N)), "Total_Currency_Obtained"

# Constraints
# Currency Exchange Limit Constraints
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= data['Limit'][i], f"Limit_Constraint_{i}"

# Starting Currency Amount Constraints
for i in range(N):
    problem += pulp.lpSum(x[j][i] * data['Rate'][j][i] for j in range(N)) <= data['Start'][i], f"Start_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')