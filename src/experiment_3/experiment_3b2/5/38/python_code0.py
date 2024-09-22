import pulp
import json

# Load data from JSON format
data = json.loads("{'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}")

# Define the problem
N = len(data['demand'])
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision Variables
reg_quant = pulp.LpVariable.dicts("RegularQuantity", range(N), lowBound=0)
over_quant = pulp.LpVariable.dicts("OvertimeQuantity", range(N), lowBound=0)
inv = pulp.LpVariable.dicts("Inventory", range(N), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['cost_regular'] * reg_quant[n] +
                       data['cost_overtime'] * over_quant[n] +
                       data['store_cost'] * inv[n] for n in range(N))

# Demand Satisfaction Constraints
for n in range(N):
    inv_prev = inv[n-1] if n > 0 else 0  # inv_0 is initialized to 0
    problem += reg_quant[n] + over_quant[n] + inv_prev == data['demand'][n] + inv[n], f"DemandConstraint_{n}"

# Regular Production Limit Constraints
for n in range(N):
    problem += reg_quant[n] <= data['max_regular_amount'], f"RegularLimit_{n}"

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')