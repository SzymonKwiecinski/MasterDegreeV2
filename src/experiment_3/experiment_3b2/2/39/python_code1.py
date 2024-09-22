import pulp
import json

# Data input
data_json = '{"num": [5, 10, 2, 3, 2, 10], "n_working_days": 5, "n_resting_days": 2}'
data = json.loads(data_json)

# Parameters
num = data['num']
N = len(num)  # number of days
M = 10  # Assuming a maximum of 10 employees for simplicity, can be adjusted

# Initialize the problem
problem = pulp.LpProblem("Minimum_Employees_Cafeteria", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(M), cat='Binary')  # Employee hired status
y = pulp.LpVariable.dicts("y", ((n, i) for n in range(N) for i in range(M)), cat='Binary')  # Employee work status

# Objective Function
problem += pulp.lpSum(x[i] for i in range(M)), "Total_Employees"

# Constraints
for n in range(N):
    problem += pulp.lpSum(y[n, i] for i in range(M)) >= num[n], f"Min_Employees_Day_{n+1}"

for n in range(N):
    for i in range(M):
        problem += y[n, i] <= x[i], f"Employee_{i+1}_Work_Day_{n+1}"

# Implement cyclic constraints for working and resting days
for i in range(M):
    for start in range(N):
        for working in range(data['n_working_days']):
            if start + working < N:
                for resting in range(data['n_resting_days']):
                    if start + working + resting < N:
                        problem += pulp.lpSum(y[j, i] for j in range(start, start + working + resting + 1)) <= data['n_working_days'], f"Cyclic_Constraint_{i+1}_{start}_{working}_{resting}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')