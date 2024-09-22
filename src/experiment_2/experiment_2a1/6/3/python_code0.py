import pulp
import json

def plan_electricity_capacity(data):
    # Parse the input data
    T = data['T']
    demand = data['Demand']
    oil_cap = data['OilCap']
    coal_cost = data['CoalCost']
    nuke_cost = data['NukeCost']
    max_nuke = data['MaxNuke'] / 100
    coal_life = data['CoalLife']
    nuke_life = data['NukeLife']
    
    # Create a linear programming problem
    problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)
    
    # Decision variables: coal and nuclear capacities added each year
    coal_cap_added = [pulp.LpVariable(f'coal_{t}', lowBound=0, cat='Continuous') for t in range(T)]
    nuke_cap_added = [pulp.LpVariable(f'nuke_{t}', lowBound=0, cat='Continuous') for t in range(T)]
    
    # Objective function: minimize total cost
    total_cost = pulp.lpSum([coal_cost * coal_cap_added[t] for t in range(T)]) + \
                 pulp.lpSum([nuke_cost * nuke_cap_added[t] for t in range(T)])
    problem += total_cost
    
    # Constraints for electricity demand and capacity
    for t in range(T):
        total_capacity = oil_cap[t]
        
        # Add coal capacity from previous years
        if t >= coal_life:
            total_capacity += pulp.lpSum(coal_cap_added[t - k] for k in range(1, coal_life + 1))
        
        # Add nuclear capacity from previous years
        if t >= nuke_life:
            total_capacity += pulp.lpSum(nuke_cap_added[t - k] for k in range(1, nuke_life + 1))
        
        # Demand constraint
        problem += total_capacity >= demand[t]
    
    # Maximum nuclear capacity constraint
    for t in range(T):
        total_capacity = oil_cap[t]
        if t >= coal_life:
            total_capacity += pulp.lpSum(coal_cap_added[t - k] for k in range(1, coal_life + 1))
        
        problem += pulp.lpSum(nuke_cap_added) <= max_nuke * total_capacity

    # Solve the problem
    problem.solve()

    # Prepare the output
    coal_added = [pulp.value(coal_cap_added[t]) for t in range(T)]
    nuke_added = [pulp.value(nuke_cap_added[t]) for t in range(T)]
    total_cost_value = pulp.value(problem.objective)

    output = {
        "coal_cap_added": coal_added,
        "nuke_cap_added": nuke_added,
        "total_cost": total_cost_value,
    }
    
    print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')
    return output

# Given input data in json format
input_data = {
    'T': 12, 
    'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 
    'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 
    'CoalCost': 10, 
    'NukeCost': 5, 
    'MaxNuke': 20, 
    'CoalLife': 5, 
    'NukeLife': 10
}

result = plan_electricity_capacity(input_data)
print(result)