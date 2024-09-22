import pulp
import json

# Data
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Problem Setup
problem = pulp.LpProblem("Minimize_Manpower_Costs", pulp.LpMinimize)

# Constants
K = len(data["requirement"])  # Manpower categories
I = len(data["requirement"][0])  # Years

# Variables
recruit = [[pulp.LpVariable(f"recruit_{k}_{i}", lowBound=0, upBound=data["recruit"][k], cat="Integer") for i in range(I)] for k in range(K)]
overmanning = [[pulp.LpVariable(f"overmanning_{k}_{i}", lowBound=0, upBound=data["num_overman"], cat="Integer") for i in range(I)] for k in range(K)]
short = [[pulp.LpVariable(f"short_{k}_{i}", lowBound=0, upBound=data["num_shortwork"], cat="Integer") for i in range(I)] for k in range(K)]

# Objective Function
total_cost = pulp.lpSum(data["costredundancy"][k] * (recruit[k][i] + overmanning[k][i]) +
                       data["costoverman"][k] * overmanning[k][i] +
                       data["costshort"][k] * short[k][i]
                       for k in range(K) for i in range(I))

problem += total_cost, "Total_Cost"

# Constraints
for k in range(K):
    current_strength = data["strength"][k]
    for i in range(I):
        if i == 0:
            prev_strength = current_strength
        else:
            prev_strength = (1 - data["lessonewaste"][k]) * recruit[k][i-1] + (1 - data["moreonewaste"][k]) * (prev_strength - recruit[k][i-1])
        
        problem += recruit[k][i] + prev_strength >= data["requirement"][k][i] - 0.5 * short[k][i] + overmanning[k][i], f"Requirement_{k}_{i}"

# Solve
problem.solve()

# Output
output = {
    "recruit": [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)]
}

print(json.dumps(output, indent=2))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')