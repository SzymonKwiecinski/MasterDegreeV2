import pulp

# Load data
data = {
    'regular_cost': 30,
    'overtime_cost': 45,
    'assembly_time': 0.4,
    'material_cost': 25,
    'selling_price': 65,
    'holding_cost': 4,
    'salvage_value': 30,
    'demand': [700, 1500, 2800, 1800],
    'regular_labor': [450, 550, 600, 600],
    'overtime_labor': [40, 200, 320, 160]
}

# Extract data
W = len(data['demand'])
regular_cost = data['regular_cost']
overtime_cost = data['overtime_cost']
assembly_time = data['assembly_time']
material_cost = data['material_cost']
selling_price = data['selling_price']
holding_cost = data['holding_cost']
salvage_value = data['salvage_value']
demand = data['demand']
regular_labor = data['regular_labor']
overtime_labor = data['overtime_labor']

# Initialize the problem
problem = pulp.LpProblem("Gift_Basket_Production", pulp.LpMaximize)

# Decision variables
regular_used = pulp.LpVariable.dicts("Regular_Used", range(W), lowBound=0)
overtime_used = pulp.LpVariable.dicts("Overtime_Used", range(W), lowBound=0)
regular_basket = pulp.LpVariable.dicts("Regular_Basket", range(W), lowBound=0)
overtime_basket = pulp.LpVariable.dicts("Overtime_Basket", range(W), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(W+1), lowBound=0)

# Objective function
profit_expression = (
    pulp.lpSum([
        (selling_price * (regular_basket[w] + overtime_basket[w]) 
         - regular_cost * regular_used[w] 
         - overtime_cost * overtime_used[w] 
         - material_cost * (regular_basket[w] + overtime_basket[w]) 
         - holding_cost * inventory[w]) 
        for w in range(W)
    ])
    + salvage_value * inventory[W]
)

problem += profit_expression

# Constraints
problem += inventory[0] == 0

for w in range(W):
    # Regular and Overtime labor constraints
    problem += regular_used[w] <= regular_labor[w]
    problem += overtime_used[w] <= overtime_labor[w]
    
    # Basket production constraints
    problem += regular_basket[w] == regular_used[w] / assembly_time
    problem += overtime_basket[w] == overtime_used[w] / assembly_time
    
    # Inventory constraint
    problem += inventory[w+1] == inventory[w] + regular_basket[w] + overtime_basket[w] - demand[w]

# Solve the problem
problem.solve()

# Display the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')