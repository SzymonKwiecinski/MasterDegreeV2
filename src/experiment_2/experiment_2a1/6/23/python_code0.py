import pulp
import json

# Input Data
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

# Define the problem
problem = pulp.LpProblem("Manpower_Management", pulp.LpMinimize)

# Variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, upBound=None, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, upBound=None, cat='Integer')
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, upBound=None, cat='Integer')

# Objective Function
cost = pulp.lpSum(
    data['costredundancy'][k] * (data['strength'][k] + pulp.lpSum(overmanning[k][i] for i in range(I)) - data['requirement'][k][i]) 
    for k in range(K) for i in range(I)) + \
    pulp.lpSum(data['costoverman'][k] * overmanning[k][i] for k in range(K) for i in range(I)) + \
    pulp.lpSum(data['costshort'][k] * short[k][i] for k in range(K) for i in range(I))

problem += cost, "Total_Cost"

# Constraints
for k in range(K):
    for i in range(I):
        problem += (
            data['strength'][k] - pulp.lpSum(recruit[k][i] for k in range(K)) +
            (1 - data['lessonewaste'][k]) * data['strength'][k] +
            (1 - data['moreonewaste'][k]) * (data['strength'][k] - pulp.lpSum(recruit[k][i-1] for i in range(1, I))) - 
            overmanning[k][i] + short[k][i] >= data['requirement'][k][i],
            f"Demand_Constraint_k{k}_i{i}"
        )
        
        problem += recruit[k][i] <= data['recruit'][k], f"Recruit_Constraint_k{k}_i{i}"
        
        if i > 0:
            problem += overmanning[k][i] <= data['num_overman'], f"Overmanning_Constraint_k{k}_i{i}"
            problem += short[k][i] <= data['num_shortwork'], f"Short_Time_Constraint_k{k}_i{i}"

# Solve the problem
problem.solve()

# Prepare Output
recruit_solution = [[int(recruit[k][i].varValue) for i in range(I)] for k in range(K)]
overmanning_solution = [[int(overmanning[k][i].varValue) for i in range(I)] for k in range(K)]
short_solution = [[int(short[k][i].varValue) for i in range(I)] for k in range(K)]

output = {
    "recruit": recruit_solution,
    "overmanning": overmanning_solution,
    "short": short_solution
}

# Print Objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')