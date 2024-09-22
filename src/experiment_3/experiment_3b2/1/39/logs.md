# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
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


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To solve the problem of scheduling employees in a cafeteria with the given constraints, we'll formulate a Mixed-Integer Linear Programming (MILP) model. The goal is to minimize the number of employees needed while ensuring the daily staffing requirements are met.

Given parameters:
- `num[n]`: The required number of employees on day \(n\).
- `n_working_days`: The number of consecutive working days for an employee.
- `n_resting_days`: The number of consecutive days off for an employee.

Decision variables:
- \(x_i\): Binary variable that indicates if employee \(i\) is hired.
- \(y_{n,i}\): Binary variable that indicates if employee \(i\) is working on day \(n\).

Objective:
Minimize \(\sum_{i} x_i\), the total number of employees hired.

Constraints:
1. Ensure that the number of employees working on any day \(n\) meets the required number: \(\sum_{i} y_{n,i} \geq num[n] \, \forall \, n\).
2. If an employee is hired, they must follow the work/rest cycle: working `n_working_days` followed by `n_resting_days`.

The mathematical model is as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Indices}

\begin{align*}
& n = 1, \ldots, N & \text{(days)} \\
& i \text{ (employee index)}
\end{align*}

\textbf{Parameters}

\begin{align*}
& num[n] & \text{(required number of employees on day } n) \\
& n\_working\_days & \text{(number of consecutive working days)} \\
& n\_resting\_days & \text{(number of consecutive resting days)}
\end{align*}

\textbf{Decision Variables}

\begin{align*}
& x_i \in \{0,1\} & \text{(1 if employee } i \text{ is hired, 0 otherwise)} \\
& y_{n,i} \in \{0,1\} & \text{(1 if employee } i \text{ works on day } n \text{, 0 otherwise)}
\end{align*}

\textbf{Objective Function}

\[
\min \sum_{i} x_i
\]

\textbf{Constraints}

\begin{align}
& \sum_{i} y_{n,i} \geq num[n], \quad \forall n \\
& y_{n,i} \leq x_i, \quad \forall n, i \\
& \text{Work/rest cycle constraints:} \\
& \left(1 - \sum_{j=0}^{n\_working\_days - 1} y_{n+j,i}\right) + \sum_{j=n\_working\_days}^{n\_working\_days+n\_resting\_days-1} y_{n+j,i} \leq n\_resting\_days \times (1-x_i), \\
& \quad \forall n, i \text{ ensuring work/rest cycle}
\end{align}

\end{document}
```

This model ensures the required staff is present each day, and adheres to the work/rest cycle constraints, while minimizing the total number of employees hired. The constraints ensure that if an employee is hired, they adhere to the working and resting pattern as specified.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Indices}

\begin{align*}
& n = 1, \ldots, N & \text{(days)} \\
& i \text{ (employee index)}
\end{align*}

\textbf{Parameters}

\begin{align*}
& num[n] & \text{(required number of employees on day } n) \\
& n\_working\_days & \text{(number of consecutive working days)} \\
& n\_resting\_days & \text{(number of consecutive resting days)}
\end{align*}

\textbf{Decision Variables}

\begin{align*}
& x_i \in \{0,1\} & \text{(1 if employee } i \text{ is hired, 0 otherwise)} \\
& y_{n,i} \in \{0,1\} & \text{(1 if employee } i \text{ works on day } n \text{, 0 otherwise)}
\end{align*}

\textbf{Objective Function}

\[
\min \sum_{i} x_i
\]

\textbf{Constraints}

\begin{align}
& \sum_{i} y_{n,i} \geq num[n], \quad \forall n \\
& y_{n,i} \leq x_i, \quad \forall n, i \\
& \text{Work/rest cycle constraints:} \\
& \left(1 - \sum_{j=0}^{n\_working\_days - 1} y_{n+j,i}\right) + \sum_{j=n\_working\_days}^{n\_working\_days+n\_resting\_days-1} y_{n+j,i} \leq n\_resting\_days \times (1-x_i), \\
& \quad \forall n, i \text{ ensuring work/rest cycle}
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'num': [5, 10, 2, 3, 2, 10],
    'n_working_days': 5,
    'n_resting_days': 2
}

num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)  #### Number of days

#### Create the LP problem
problem = pulp.LpProblem("Employee_Scheduling_Problem", pulp.LpMinimize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(N), cat='Binary')  #### Employee hired
y = pulp.LpVariable.dicts("y", (range(N), range(N)), cat='Binary')  #### Employee work schedule

#### Objective function: Minimize number of employees hired
problem += pulp.lpSum(x[i] for i in range(N))

#### Constraints
#### 1. Required number of employees for each day
for n in range(N):
    problem += pulp.lpSum(y[n][i] for i in range(N)) >= num[n]

#### 2. An employee can only work if they are hired
for n in range(N):
    for i in range(N):
        problem += y[n][i] <= x[i]

#### 3. Work/rest cycle constraints
for i in range(N):
    for n in range(N - n_working_days - n_resting_days + 1):
        problem += (1 - pulp.lpSum(y[n + j][i] for j in range(n_working_days))) + \
                   pulp.lpSum(y[n + j][i] for j in range(n_working_days, n_working_days + n_resting_days)) <= \
                   n_resting_days * (1 - x[i])

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

