import pulp
import json

# Data from JSON format
data = json.loads('{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}')

N = data['N']
Start = data['Start']
Limit = data['Limit']
Rate = data['Rate']

# Create the LP problem
problem = pulp.LpProblem("Currency_Exchange_Problem", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), lowBound=0)

# Objective function: Maximize total amount of currency N
problem += pulp.lpSum(x[N-1][j] for j in range(N)), "Total_Amount"

# Constraints for each currency
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= Limit[i], f"Limit_Constraint_{i}"
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= Start[i], f"Start_Constraint_{i}"
    problem += Start[i] + pulp.lpSum(x[j][i] for j in range(N)) - pulp.lpSum(x[i][j] for j in range(N)) == pulp.LpVariable(f'final_{i}'), f"Flow_Conservation_{i}"

# Exchange rate constraints
for i in range(N):
    for j in range(N):
        if i != j:
            problem += x[i][j] * Rate[i][j] <= x[j][i], f"Rate_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')