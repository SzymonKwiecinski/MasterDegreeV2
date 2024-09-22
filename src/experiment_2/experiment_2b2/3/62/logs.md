# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MILP

PROBLEM INFO:

- A traveler based in \var{start_city} needs to visit \var{N} towns for business.
- The distance \var{distance_{i,j}} between city \var{i} and \var{j} is provided in miles and are symmetric, meaning the distance from city \var{i} to city \var{j} is the same as from city \var{j} to city \var{i}.
- The traveler must return to \var{start_city} after visiting all towns.

INPUT FORMAT: 

{
    "distances": {
        city_i: {
            city_j: distance_{i, j},
            for j in 1, ..., N-1
        },
        for i in 1, ..., N
    },
    "start_city": start_city
}

OBJECTIVE: Determine the shortest route that the traveler can take to visit all \var{N} towns and return to \var{start_city}.

OUTPUT INFO:

- The sequence of cities visited after \var{start_city} is \var{visit_order}.
- \var{total_distance} traveled on this optimal journey.

OUTPUT FORMAT:

{
    "visit_order": [city_n for n in 1, ..., N+1],
    "total_distance": total_distance
}
</DESCRIPTION>
<DATA>
{'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To solve the traveling salesman problem (TSP) described, we'll utilize the Pulp library to formulate it as a Mixed-Integer Linear Programming (MILP) problem. The goal is to minimize the total distance traveled starting and ending at the specified `StartCity`.

Here's the Python code that does this:

```python
import pulp

def solve_tsp(data):
    N = data['N']
    distances = data['Distances']
    start_city = data['StartCity']

    #### Create the problem
    problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

    #### Variables: x[i][j] is 1 if the route goes from city i to city j
    x = [[pulp.LpVariable(f"x_{i}_{j}", cat='Binary') for j in range(N)] for i in range(N)]

    #### Objective function: Minimize the total distance
    problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N) if i != j)

    #### Constraints
    #### Each city must be entered once, except the start city which is entered N times
    for i in range(N):
        if i == start_city:
            problem += pulp.lpSum(x[j][i] for j in range(N) if j != i) == N
        else:
            problem += pulp.lpSum(x[j][i] for j in range(N) if j != i) == 1

    #### Each city must be exited once, except the start city which is exited N times
    for j in range(N):
        if j == start_city:
            problem += pulp.lpSum(x[j][i] for i in range(N) if i != j) == N
        else:
            problem += pulp.lpSum(x[j][i] for i in range(N) if i != j) == 1

    #### Subtour elimination
    u = [pulp.LpVariable(f"u_{i}", cat='Integer', lowBound=0, upBound=N-1) for i in range(N)]
    for i in range(1, N):
        for j in range(1, N):
            if i != j:
                problem += u[i] - u[j] + (N * x[i][j]) <= N - 1    

    #### Solve the problem
    problem.solve()

    #### Extract the solution
    visit_order = [start_city]
    current_city = start_city

    for _ in range(N):
        for j in range(N):
            if pulp.value(x[current_city][j]) == 1:
                visit_order.append(j)
                current_city = j
                break

    #### Determine total distance
    total_distance = pulp.value(problem.objective)

    return {
        "visit_order": visit_order,
        "total_distance": total_distance
    }


#### Define input data
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}

#### Solve the TSP
result = solve_tsp(data)
print(result)
print(f' (Objective Value): <OBJ>{result["total_distance"]}</OBJ>')
```

This solution will provide the optimal route and the total distance for the traveling salesman problem given the provided distances.

