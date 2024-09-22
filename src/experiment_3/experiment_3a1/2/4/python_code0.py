import pulp
import json

# Load data
data = json.loads('{"T": 7, "Period": 4, "Demand": [0, 5, 9, 15, 4, 7, 3]}')
T = data['T']
period = data['Period']
demand = data['Demand']

# Define the problem
problem = pulp.LpProblem("Nurse_Scheduling_Problem", pulp.LpMinimize)

# Decision variables
start = [pulp.LpVariable(f'start_{j}', lowBound=0, cat='Integer') for j in range(1, T + 1)]
N = pulp.LpVariable('N', lowBound=0, cat='Integer')

# Objective function
problem += N, "Total_Nurses_Hired"

# Constraints for meeting demand
for j in range(1, T + 1):
    demand_constraints = pulp.lpSum(start[max(0, j - k - 1)] for k in range(period))  # Adjust for zero-based index
    problem += demand_constraints >= demand[j - 1], f"Demand_Constraint_day_{j}"

# Objective value calculation
problem += pulp.lpSum(start[j - 1] for j in range(1, T + 1)) == N, "Total_Nurses_Equivalence"

# Solve the problem
problem.solve()

# Output
start_values = [start[j].varValue for j in range(T)]
total_nurses_hired = pulp.value(N)

print(f'Start values: {start_values}')
print(f'Total Nurses Hired: {total_nurses_hired}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')