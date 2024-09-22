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
To solve this problem, we will use the Pulp library to formulate a linear programming model. The goal is to determine the minimum number of employees needed to meet the daily staffing requirements over a series of days, where each employee works a specified number of consecutive days and then rests for another specified number of consecutive days.

Here's the implementation:

```python
import pulp

#### Data from the problem
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']

#### Number of days
N = len(num)

#### Problem
problem = pulp.LpProblem("MinimizeEmployees", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("Employee_", range(N), 0, cat=pulp.LpInteger)

#### Objective function: Minimize the total number of employees (sum of x)
problem += pulp.lpSum(x[i] for i in range(N)), "TotalEmployees"

#### Constraints
for day in range(N):
    problem += pulp.lpSum(x[(day - start) % N] for start in range(n_working_days)) >= num[day], f"StaffRequirement_day{day}"

#### Solve the problem
problem.solve()

#### Extract the results
total_number = sum(x[i].varValue for i in range(N))
is_work = [[0]*N for _ in range(int(total_number))]

#### Assign working days to each employee
employee_counter = 0
for start in range(N):
    for e in range(int(x[start].varValue)):
        for k in range(n_working_days):
            is_work[employee_counter][(start + k) % N] = 1
        employee_counter += 1

#### Format the result
result = {
    "total_number": int(total_number),
    "is_work": is_work
}

result
```

This code sets up the problem using the Pulp library. It minimizes the total number of employees while ensuring that the staffing numbers on each day meet or exceed the requirements specified in the `num` array. Each employee works `n_working_days` followed by `n_resting_days`. The `is_work` matrix in the result highlights the working days for each hired employee across the days.

