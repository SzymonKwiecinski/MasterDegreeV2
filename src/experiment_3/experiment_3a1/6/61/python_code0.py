import pulp
import json

# Data from JSON
data = {
    'processing_times': {
        'central': {'isolate': [10, 6, 8], 'scan': [6, 4, 6]},
        'distributed': {'isolate': [12, 9, 12], 'scan': [18, 10, 15]}
    },
    'costs': {'central': 150, 'distributed': 70},
    'max_hours': {'central_max_hours': 16, 'distributed_max_hours': 33}
}

# Extracting data
N = len(data['processing_times']['central']['isolate'])
isolate_central = data['processing_times']['central']['isolate']
scan_central = data['processing_times']['central']['scan']
isolate_distributed = data['processing_times']['distributed']['isolate']
scan_distributed = data['processing_times']['distributed']['scan']
central_cost = data['costs']['central']
distributed_cost = data['costs']['distributed']
max_central = data['max_hours']['central_max_hours']
max_distributed = data['max_hours']['distributed_max_hours']

# Create the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision Variables
x_c = [pulp.LpVariable(f'x_{i+1}^c', lowBound=0, upBound=1) for i in range(N)]  # Isolation central
y_c = [pulp.LpVariable(f'y_{i+1}^c', lowBound=0, upBound=1) for i in range(N)]  # Scan central
x_d = [pulp.LpVariable(f'x_{i+1}^d', lowBound=0, upBound=1) for i in range(N)]  # Isolation distributed
y_d = [pulp.LpVariable(f'y_{i+1}^d', lowBound=0, upBound=1) for i in range(N)]  # Scan distributed
z = [pulp.LpVariable(f'z_{i+1}', cat='Binary') for i in range(N)]  # Intervention type

# Objective Function
problem += pulp.lpSum([
    central_cost * (x_c[i] * isolate_central[i] + y_c[i] * scan_central[i]) +
    distributed_cost * (x_d[i] * isolate_distributed[i] + y_d[i] * scan_distributed[i])
    for i in range(N)
]), "Total_Cost"

# Constraints
problem += pulp.lpSum([x_c[i] * isolate_central[i] + y_c[i] * scan_central[i] for i in range(N)]) <= max_central, "Max_Central_Hours"
problem += pulp.lpSum([x_d[i] * isolate_distributed[i] + y_d[i] * scan_distributed[i] for i in range(N)]) <= max_distributed, "Max_Distributed_Hours"
for i in range(N):
    problem += x_c[i] + x_d[i] <= 1, f"Isolation_Constraint_{i+1}"
    problem += y_c[i] + y_d[i] <= 1, f"Scan_Constraint_{i+1}"

# Solve the problem
problem.solve()

# Output result
interventions = []
for i in range(N):
    if pulp.value(z[i]) == 1:
        interventions.append({
            'cluster_id': i + 1,
            'type': 'isolate',
            'method': 'central' if pulp.value(x_c[i]) > 0 else 'distributed',
            'amount': pulp.value(x_c[i]) if pulp.value(x_c[i]) > 0 else pulp.value(x_d[i])
        })
    else:
        interventions.append({
            'cluster_id': i + 1,
            'type': 'scan',
            'method': 'central' if pulp.value(y_c[i]) > 0 else 'distributed',
            'amount': pulp.value(y_c[i]) if pulp.value(y_c[i]) > 0 else pulp.value(y_d[i])
        })

total_cost = pulp.value(problem.objective)

print(interventions)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')