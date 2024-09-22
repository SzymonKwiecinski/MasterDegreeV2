import pulp
import json

# Load data from JSON format
data = json.loads("{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}")

# Parameters
T = data['T']  # Number of days
period = data['Period']  # Number of consecutive days a nurse works
demand = data['Demand']  # Demand for nurses for the week

# Create the LP problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Nurses_starting_day", range(1, T + 1), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(x[j] for j in range(1, T + 1)), "Total_Nurses_Hired"

# Constraints
for j in range(1, T + 1):
    problem += pulp.lpSum(x[(j - k - 1) % T + 1] for k in range(period)) >= demand[j - 1], f"Demand_Constraint_day_{j}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')