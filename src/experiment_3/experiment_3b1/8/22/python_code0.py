import pulp

# Data from JSON
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

# Indices
K = len(data['strength'])  # number of categories
I = len(data['requirement'])  # number of years

# Create the linear programming problem
problem = pulp.LpProblem("Manpower_Management", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0)
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0)
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * (recruit[k][i] - data['requirement'][i][k]) for k in range(K) for i in range(I) if recruit[k][i] > data['requirement'][i][k]), "Total_Redundancy_Cost"

# Constraints
for i in range(I):
    for k in range(K):
        # Manpower Balance Constraint
        problem += (data['strength'][k] + recruit[k][i] - overmanning[k][i] - short[k][i] * 0.5 >= data['requirement'][i][k]), f"Manpower_Balance_Constraint_k{k}_i{i}"
        
        # Recruitment Limitations
        problem += (recruit[k][i] <= data['recruit'][k]), f"Recruitment_Limit_k{k}_i{i}"

        # Short-time Working Limitations
        problem += (short[k][i] <= data['num_shortwork']), f"Short_Time_Work_Limit_k{k}_i{i}"

# Overmanning Limitations
for i in range(I):
    problem += (pulp.lpSum(overmanning[k][i] for k in range(K)) <= data['num_overman']), f"Overmanning_Limit_i{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')