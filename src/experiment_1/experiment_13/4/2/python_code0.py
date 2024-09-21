import pulp
import json

# Data
data = json.loads("{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}")
T = data['T']
Demand = data['Demand']

# Create the LP problem
problem = pulp.LpProblem("Nurse_Staffing_Problem", pulp.LpMinimize)

# Decision variable
N = pulp.LpVariable("N", lowBound=0, cat='Continuous')  # Number of nurses to hire

# Objective function
problem += N, "Minimize_Nurses"

# Constraints
for t in range(T):
    problem += N >= Demand[t], f"Demand_Constraint_{t+1}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')