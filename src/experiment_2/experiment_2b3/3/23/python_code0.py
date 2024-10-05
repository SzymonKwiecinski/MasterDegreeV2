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

K = len(data['strength'])  # Number of manpower types
I = len(data['requirement'][0])  # Number of years

# Problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Variables
recruit_var = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning_var = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short_var = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective Function
total_cost = (
    pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] * data['moreonewaste'][k])
    for k in range(K))  # Initial state redundancy
    + pulp.lpSum(data['costoverman'][k] * overmanning_var[k, i]
    + data['costshort'][k] * short_var[k, i]
    for k in range(K) for i in range(I))
)

problem += total_cost, "Total Cost"

# Constraints for each year and each manpower type
for k in range(K):
    workers_current_year = data['strength'][k]
    for i in range(I):
        if i > 0:
            workers_current_year = (
                (workers_current_year - data['requirement'][k][i-1]) * (1 - data['lessonewaste'][k])
            )

        # Worker count must satisfy or exceed the requirement
        problem += (
            workers_current_year + recruit_var[k, i] + overmanning_var[k, i]
            - short_var[k, i] >= data['requirement'][k][i]
        )
        
        # Overmanning limit
        problem += overmanning_var[k, i] <= data['num_overman']
        
        # Short-time working limit
        problem += short_var[k, i] <= data['num_shortwork']
        
        # Recruitment limit
        problem += recruit_var[k, i] <= data['recruit'][k]

# Solve the problem
problem.solve()

# Results
output = {
    "recruit": [[pulp.value(recruit_var[k, i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning_var[k, i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short_var[k, i]) for i in range(I)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')