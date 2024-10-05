# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP or MILP
PROBLEM INFO:

- To operate a cafeteria, the manager must ensure on-call duty based on the statistics on the required staff. 
- In the future days, the number of desired employees on day \var{n} is denoted with \var{num_{n}}.
- Each employee works \var{n_working_days} days in a row and then has \var{n_resting_days} days off.

INPUT FORMAT:

{
	"num": [num_{n} for n in 1,...,N],
	"n_working_days": n_working_days,
	"n_resting_days": n_resting_days
}


OBJECTIVE: Calculate the minimum number of employees to hire

OUTPUT INFO:

- \var{total_number} represents the total number of employees to employ
- \var{is_work} represents whether employee is working a rest on each day. Its length is determined by \var{total_number}

OUTPUT FORMAT:

{
	"total_number": total_number,
	"is_work": [[is_work_{n, i} for n in 1,...,N] for i in 1,...,total_number]
}
</DESCRIPTION>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the problem
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

#### Problem parameters
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

#### Initialize the linear programming problem
problem = pulp.LpProblem("Minimize_Employees", pulp.LpMinimize)

#### Decision Variables
#### Binary variables indicating if employee i starts working on day n
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat=pulp.LpBinary)

#### Objective Function
problem += pulp.lpSum(x[n][i] for n in range(N) for i in range(N)), "Total_Employees"

#### Constraints
#### Ensure enough employees are working each day
for n in range(N):
    problem += (pulp.lpSum(x[i][((n-i) % N)] for i in range(N) if i <= n or i >= n-N+n_working_days) >= num[n]), f"Demand_Constraint_day_{n+1}"

#### Solve the problem
problem.solve()

#### Extract the total number of employees required
total_number = sum(pulp.value(x[n][i]) for n in range(N) for i in range(N))

#### Extract working schedule
is_work = [[int(i == pulp.value(x[i][(n-i) % N])) for n in range(N)] for i in range(N)]

#### Output the results in the specified format
output = {
    "total_number": int(total_number),
    "is_work": is_work
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


