import pulp
import json

# Data in JSON format
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
K = len(data['strength'])  # number of manpower categories
I = len(data['requirement'])  # number of years

# Create the Linear Programming problem
problem = pulp.LpProblem("Manpower_Management", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
overmanning_vars = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
short_vars = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - (data['strength'][k] * data['moreonewaste'][k]) - short_vars[(k, i)] + recruit_vars[(k, i)] + overmanning_vars[(k, i)] for i in range(I)) for k in range(K)) + \
            pulp.lpSum(data['costoverman'][k] * pulp.lpSum(overmanning_vars[(k, i)] for i in range(I)) for k in range(K)) + \
            pulp.lpSum(data['costshort'][k] * pulp.lpSum(short_vars[(k, i)] for i in range(I)) for k in range(K)), "Total_Cost"

# Constraints
for i in range(I):
    for k in range(K):
        # Manpower availability for year i
        problem += (data['strength'][k] - (data['strength'][k] * data['moreonewaste'][k]) - short_vars[(k, i)] + recruit_vars[(k, i)] + overmanning_vars[(k, i)] == data['requirement'][i][k], f"Availability_Constraint_{k}_{i}")

        # Recruitment Limit
        problem += (recruit_vars[(k, i)] <= data['recruit'][k], f"Recruitment_Limit_{k}_{i}")
        
        # Short-time working Limit
        problem += (short_vars[(k, i)] <= data['num_shortwork'], f"Short_Time_Working_Limit_{k}_{i}")

# Overmanning Limit
for i in range(I):
    problem += (pulp.lpSum(overmanning_vars[(k, i)] for k in range(K)) <= data['num_overman'], f"Overmanning_Limit_{i}")

# Solve the problem
problem.solve()

# Output objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')