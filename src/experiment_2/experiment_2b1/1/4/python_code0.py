import pulp
import json

# Data input
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}

# Parameters
T = data['T']
period = data['Period']
demand = data['Demand']

# Define the problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision Variables
start = pulp.LpVariable.dicts("start", range(T), lowBound=0, cat='Integer')

# Objective Function: Minimize the total number of nurses hired
total_nurses = pulp.lpSum([start[j] for j in range(T)])
problem += total_nurses

# Constraints
for j in range(T):
    # Demand must be satisfied for each day
    problem += (pulp.lpSum(start[(j - k) % T] for k in range(period)) >= demand[j]), f"Demand_Constraint_Day_{j}"

# Solve the problem
problem.solve()

# Get results
result = {
    "start": [int(start[j].value()) for j in range(T)],
    "total": int(pulp.value(problem.objective))
}

# Output
print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')