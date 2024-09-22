import pulp
import json

data = {
    'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]],
    'strength': [2000, 1500, 1000],
    'lessonewaste': [0.25, 0.2, 0.1],
    'moreonewaste': [0.1, 0.05, 0.05],
    'recruit': [500, 800, 500],
    'costredundancy': [200, 500, 500],
    'num_overman': 150,
    'costoverman': [1500, 2000, 3000],
    'num_shortwork': 50,
    'costshort': [500, 400, 400]
}

K = len(data['strength'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Create the LP problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("Recruit", (range(K), range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("Overmanning", (range(K), range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("Short", (range(K), range(I)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - 
            (data['requirement'][k][i] + overmanning[k][i] + 
            (short[k][i] / 2)) + 
            recruit[k][i]) for k in range(K) for i in range(I)), "Total_Redundancy_Cost"

# Constraints
for i in range(I):
    for k in range(K):
        problem += (pulp.lpSum(recruit[k][j] for j in range(i + 1)) +
                    data['strength'][k] * (1 - data['moreonewaste'][k]) + 
                    overmanning[k][i] + 
                    (short[k][i] / 2) >= data['requirement'][k][i]), f"Requirement_Constraint_k_{k}_year_{i}")

        problem += (recruit[k][i] <= data['recruit'][k], f"Recruit_Limit_k_{k}_year_{i}")
        problem += (overmanning[k][i] <= data['num_overman'], f"Overmanning_Limit_k_{k}_year_{i}")
        problem += (short[k][i] <= data['num_shortwork'], f"Short_Work_Limit_k_{k}_year_{i}")

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "recruit": [[int(recruit[k][i].varValue) for i in range(I)] for k in range(K)],
    "overmanning": [[int(overmanning[k][i].varValue) for i in range(I)] for k in range(K)],
    "short": [[int(short[k][i].varValue) for i in range(I)] for k in range(K)],
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print the output
print(json.dumps(output))