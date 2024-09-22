import pulp
import json

# Data input
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
Period = data['Period']
Demand = data['Demand']

# Create a linear programming problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(1, T + 1), lowBound=0, cat='Integer')

# Objective function: Minimize total number of nurses hired
problem += pulp.lpSum(x[j] for j in range(1, T + 1)), "Total_Nurses_Hired"

# Constraints to meet demand for each day
for j in range(1, T + 1):
    problem += (
        pulp.lpSum(x[(j - k) % T + 1] for k in range(Period)) >= Demand[j - 1],
        f"Demand_Constraint_Day_{j}"
    )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')