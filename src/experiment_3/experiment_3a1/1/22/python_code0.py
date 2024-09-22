import pulp
import json

# Data from JSON format
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

# Parameters
K = len(data['strength'])  # number of worker types
I = len(data['requirement'])  # number of years

# Create the problem
problem = pulp.LpProblem("Minimize_Redundancy_Costs", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * (recruit[k][i] + overmanning[k][i] - short[k][i]) for k in range(K) for i in range(I)), "Total_Redundancy_Cost"

# Constraints
# Manpower Requirements
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] - 
                    data['lessonewaste'][k] * data['strength'][k] - 
                    data['moreonewaste'][k] * data['strength'][k] + 
                    recruit[k][i] + 
                    overmanning[k][i] - 
                    short[k][i] >= 
                    data['requirement'][i][k], 
                    f"Manpower_Requirement_k{k}_i{i}")

# Recruitment Limit
for k in range(K):
    for i in range(I):
        problem += (recruit[k][i] <= data['recruit'][k], 
                    f"Recruitment_Limit_k{k}_i{i}")

# Overmanning Limit
problem += (pulp.lpSum(overmanning[k][i] for k in range(K) for i in range(I)) <= data['num_overman'],
            "Overmanning_Limit")

# Short-time Working Limit
for k in range(K):
    for i in range(I):
        problem += (short[k][i] <= data['num_shortwork'], 
                    f"Short_Work_Limit_k{k}_i{i}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')