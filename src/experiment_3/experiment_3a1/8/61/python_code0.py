import pulp
import json

# Input data
data_json = '''{
    "processing_times": {
        "central": {
            "isolate": [10, 6, 8],
            "scan": [6, 4, 6]
        },
        "distributed": {
            "isolate": [12, 9, 12],
            "scan": [18, 10, 15]
        }
    },
    "costs": {
        "central": 150,
        "distributed": 70
    },
    "max_hours": {
        "central_max_hours": 16,
        "distributed_max_hours": 33
    }
}'''

data = json.loads(data_json)

# Model setup
N = len(data['processing_times']['central']['isolate'])  # Number of clusters
problem = pulp.LpProblem("MILP_Intervention_Cost_Minimization", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", 
                           ((i, j, k) for i in range(N) for j in ['isolate', 'scan'] for k in ['central', 'distributed']),
                           cat='Binary')

# Objective Function
total_cost = pulp.lpSum(data['costs'][k] * x[(i, j, k)] * data['processing_times'][k][j][i] 
                                               for i in range(N) 
                                               for j in ['isolate', 'scan'] 
                                               for k in ['central', 'distributed'])
problem += total_cost, "Total_Cost"

# Constraints
# Processing Time Constraints
for i in range(N):
    problem += (pulp.lpSum(data['processing_times']['central'][j][i] * x[(i, j, 'central')] for j in ['isolate', 'scan']) 
                 <= data['max_hours']['central_max_hours']), f"Central_Time_Constraint_{i}"
    
    problem += (pulp.lpSum(data['processing_times']['distributed'][j][i] * x[(i, j, 'distributed')] for j in ['isolate', 'scan']) 
                 <= data['max_hours']['distributed_max_hours']), f"Distributed_Time_Constraint_{i}"

# Intervention Type Consistency
for i in range(N):
    problem += (pulp.lpSum(x[(i, j, k)] for j in ['isolate', 'scan'] for k in ['central', 'distributed']) 
                 == 1), f"Intervention_Type_Constraint_{i}"

# Solve the problem
problem.solve()

# Output the results
interventions = [(i, j, k) for i in range(N) for j in ['isolate', 'scan'] for k in ['central', 'distributed'] if pulp.value(x[(i, j, k)]) == 1]
total_cost_value = pulp.value(problem.objective)

print(f'Interventions: {interventions}')
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')