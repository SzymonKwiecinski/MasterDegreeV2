import pulp

# Data
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

K = len(data['strength'])
I = len(data['requirement'][0])

# Create the problem
problem = pulp.LpProblem("Minimize_Redundancy_Cost", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0)
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0)
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0)
redundancy = pulp.LpVariable.dicts("redundancy", (range(K), range(I)), lowBound=0)

# Objective Function
problem += pulp.lpSum(redundancy[k][i] * data['costredundancy'][k] for k in range(K) for i in range(I)), "Total_Redundancy_Cost"

# Constraints
for k in range(K):
    for i in range(I):
        if i == 0:
            problem += (data['strength'][k] + recruit[k][i] - redundancy[k][i] * (1 - data['moreonewaste'][k]) +
                         overmanning[k][i] + 0.5 * short[k][i] >= data['requirement'][k][i]), f"Manpower_Balance_{k}_{i}"
        else:
            problem += (data['requirement'][k][i-1] + recruit[k][i] - redundancy[k][i] * (1 - data['moreonewaste'][k]) +
                         overmanning[k][i] + 0.5 * short[k][i] >= data['requirement'][k][i]), f"Manpower_Balance_{k}_{i}"

        # Recruitment Limit
        problem += (recruit[k][i] <= data['recruit'][k]), f"Recruitment_Limit_{k}_{i}"

        # Overmanning Limit
        problem += (overmanning[k][i] <= data['num_overman']), f"Overmanning_Limit_{k}_{i}"

        # Short-time Working Limit
        problem += (short[k][i] <= data['num_shortwork']), f"Shorttime_Working_Limit_{k}_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')