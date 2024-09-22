import pulp
import json

# Data input
data = json.loads('{"N": 2, "AssemblyHour": [0.25, 0.3333], "TestingHour": [0.125, 0.3333], "MaterialCost": [1.2, 0.9], "MaxAssembly": 10, "MaxTesting": 70, "Price": [9, 8], "MaxOvertimeAssembly": 50, "OvertimeAssemblyCost": 5, "MaterialDiscount": 10, "DiscountThreshold": 300}')

# Parameters
N = data['N']
A = data['AssemblyHour']
T = data['TestingHour']
M = data['MaterialCost']
max_assembly = data['MaxAssembly']
max_testing = data['MaxTesting']
P = data['Price']
max_overtime_assembly = data['MaxOvertimeAssembly']
overtime_assembly_cost = data['OvertimeAssemblyCost']
material_discount = data['MaterialDiscount']
discount_threshold = data['DiscountThreshold']

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Integer')
o = pulp.LpVariable("o", lowBound=0, upBound=max_overtime_assembly)

# Objective function
C_m = pulp.lpSum(M[i] * x[i] for i in range(N))
discounted_C_m = pulp.lpSum(M[i] * x[i] * (1 - material_discount / 100) for i in range(N))

# Use a conditional check for the objective function
C_m_expr = C_m - (discounted_C_m - C_m) * pulp.lpSum((C_m < discount_threshold))

Z = pulp.lpSum(P[i] * x[i] for i in range(N)) - (C_m_expr + overtime_assembly_cost * o)
problem += Z, "Objective"

# Constraints
problem += pulp.lpSum(A[i] * x[i] for i in range(N)) <= max_assembly + o, "Assembly_Constraint"
problem += pulp.lpSum(T[i] * x[i] for i in range(N)) <= max_testing, "Testing_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')