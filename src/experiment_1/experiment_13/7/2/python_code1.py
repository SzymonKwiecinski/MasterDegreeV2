import pulp
import json

# Load data from JSON format.
data = json.loads('{"T": 7, "Period": 4, "Demand": [0, 5, 9, 15, 4, 7, 3]}')

# Parameters
T = data['T']
Demand = data['Demand']

# Create a linear programming problem
problem = pulp.LpProblem("Nurse_Staffing_Problem", pulp.LpMinimize)

# Decision variable for the number of nurses to hire
N = pulp.LpVariable("N", lowBound=0, cat='Continuous')

# Objective function
problem += N

# Constraints
for t in range(T):
    problem += (N >= Demand[t], f"Demand_Constraint_{t+1}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')