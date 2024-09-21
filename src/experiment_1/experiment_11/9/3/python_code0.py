import pulp
import json

# Input Data
data = {
    'NumParts': 5,
    'NumMachines': 2,
    'Time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'Profit': [30, 20, 40, 25, 10],
    'Capacity': [700, 1000]
}

# Parameters
NumParts = data['NumParts']
NumMachines = data['NumMachines']
Time = data['Time']
Profit = data['Profit']
Capacity = data['Capacity']

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(NumParts), lowBound=0)

# Objective Function
problem += pulp.lpSum(Profit[k] * x[k] for k in range(NumParts)), "Total_Profit"

# Constraints
for s in range(NumMachines):
    problem += pulp.lpSum(Time[k][s] * x[k] for k in range(NumParts)) <= Capacity[s], f"Machine_Capacity_{s+1}"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')