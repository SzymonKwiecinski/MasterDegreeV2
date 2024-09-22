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

K = len(data['strength'])
I = len(data['requirement'][0])

# Create the problem
problem = pulp.LpProblem("Redundancy_Minimization_Problem", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
redundancy = pulp.LpVariable.dicts("redundancy", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0)
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * redundancy[k, i] for k in range(K) for i in range(I)), "Total_Redundancy_Cost"

# Constraints
for k in range(K):
    for i in range(I):
        # Manpower Balance
        problem += (
            data['strength'][k] + 
            pulp.lpSum(recruit[k, j] * (1 - data['lessonewaste'][k])**max(0, i-j) * (1 - data['moreonewaste'][k])**(i-j-1) for j in range(i+1)) -
            redundancy[k, i] + overmanning[k, i] + 0.5 * short[k, i] >= data['requirement'][k][i]
        ), f"Manpower_Balance_k{k}_i{i}"
        
        # Recruitment Constraints
        problem += recruit[k, i] <= data['recruit'][k], f"Recruitment_Constraint_k{k}_i{i}"
        
        # Short-Time Working Constraints
        problem += short[k, i] <= data['num_shortwork'], f"Short_Working_Constraint_k{k}_i{i}"

# Overmanning Constraints
for i in range(I):
    problem += pulp.lpSum(overmanning[k, i] for k in range(K)) <= data['num_overman'], f"Overmanning_Constraint_i{i}"

# Solve the problem
problem.solve()

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')