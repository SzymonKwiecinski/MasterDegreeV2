import pulp
import numpy as np

# Data from the provided JSON
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

# Create the linear programming problem
problem = pulp.LpProblem("Manpower_Management", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("Recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
overmanning = pulp.LpVariable.dicts("Overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
short = pulp.LpVariable.dicts("Short", ((k, i) for k in range(K) for i in range(I)), lowBound=0)

# Objective Function
problem += pulp.lpSum(
    data['costredundancy'][k] * pulp.lpMax(0, data['strength'][k] - data['requirement'][k][i]) +
    data['costoverman'][k] * overmanning[k, i] +
    data['costshort'][k] * short[k, i] 
    for k in range(K) for i in range(I)
), "Total_Cost"

# Constraints
for k in range(K):
    for i in range(I):
        problem += (
            data['strength'][k] -
            data['lessonewaste'][k] * recruit[k, i] -
            data['moreonewaste'][k] * data['strength'][k] +
            recruit[k, i] + 
            overmanning[k, i] + 
            short[k, i] / 2 >= data['requirement'][k][i],
            f"Manpower_Balance_{k}_{i}"
        )

for k in range(K):
    problem += (
        pulp.lpSum(recruit[k, i] for i in range(I)) <= data['recruit'][k],
        f"Recruitment_Limit_{k}"
    )

for k in range(K):
    problem += (
        pulp.lpSum(overmanning[k, i] for i in range(I)) <= data['num_overman'],
        f"Overmanning_Limit_{k}"
    )

for k in range(K):
    problem += (
        pulp.lpSum(short[k, i] for i in range(I)) <= data['num_shortwork'],
        f"Short_Time_Working_Limit_{k}"
    )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')