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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Cafeteria Staffing Problem}

\textbf{Variables:}
\begin{itemize}
    \item Let \( N \) be the total number of days.
    \item Let \( num_n \) be the number of required employees on day \( n \), for \( n = 1, 2, \ldots, N \).
    \item Let \( total\_number \) be the total number of employees to hire.
    \item Let \( n\_working\_days \) be the number of consecutive working days for each employee.
    \item Let \( n\_resting\_days \) be the number of consecutive resting days for each employee.
    \item Define \( is\_work_{n,i} \) as a binary variable that indicates if employee \( i \) is working on day \( n \) (1 if working, 0 if resting).
\end{itemize}

\textbf{Objective:}
\begin{align*}
    \text{Minimize } & total\_number
\end{align*}

\textbf{Constraints:}
For each day \( n \) (from 1 to \( N \)):
\begin{align*}
    \sum_{i=1}^{total\_number} is\_work_{n,i} & \geq num_n \quad \forall n 
\end{align*}

To ensure each employee works for \( n\_working\_days \) and rests for \( n\_resting\_days \):
\begin{align*}
    is\_work_{n,i} + is\_work_{n+1,i} + \ldots + is\_work_{n+n\_working\_days-1,i} & = n\_working\_days \quad \forall i, n \text{ such that } n + n\_working\_days - 1 \leq N \\
    is\_work_{n+n\_working\_days,i} + is\_work_{n+n\_working_days+1,i} + \ldots + is\_work_{n+n\_working_days+n\_resting\_days-1,i} & = 0 \quad \forall i, n \text{ such that } n + n\_working\_days + n\_resting\_days - 1 \leq N
\end{align*}

\textbf{Output:}
\begin{align*}
    \text{Output } & \{total\_number, is\_work_{n,i} \text{ for } n=1,\ldots,N \text{ and } i=1,\ldots,total\_number\}
\end{align*}

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Cafeteria Staffing Problem}

\textbf{Variables:}
\begin{itemize}
    \item Let \( N \) be the total number of days.
    \item Let \( num_n \) be the number of required employees on day \( n \), for \( n = 1, 2, \ldots, N \).
    \item Let \( total\_number \) be the total number of employees to hire.
    \item Let \( n\_working\_days \) be the number of consecutive working days for each employee.
    \item Let \( n\_resting\_days \) be the number of consecutive resting days for each employee.
    \item Define \( is\_work_{n,i} \) as a binary variable that indicates if employee \( i \) is working on day \( n \) (1 if working, 0 if resting).
\end{itemize}

\textbf{Objective:}
\begin{align*}
    \text{Minimize } & total\_number
\end{align*}

\textbf{Constraints:}
For each day \( n \) (from 1 to \( N \)):
\begin{align*}
    \sum_{i=1}^{total\_number} is\_work_{n,i} & \geq num_n \quad \forall n 
\end{align*}

To ensure each employee works for \( n\_working\_days \) and rests for \( n\_resting\_days \):
\begin{align*}
    is\_work_{n,i} + is\_work_{n+1,i} + \ldots + is\_work_{n+n\_working\_days-1,i} & = n\_working\_days \quad \forall i, n \text{ such that } n + n\_working\_days - 1 \leq N \\
    is\_work_{n+n\_working\_days,i} + is\_work_{n+n\_working_days+1,i} + \ldots + is\_work_{n+n\_working_days+n\_resting\_days-1,i} & = 0 \quad \forall i, n \text{ such that } n + n\_working\_days + n\_resting\_days - 1 \leq N
\end{align*}

\textbf{Output:}
\begin{align*}
    \text{Output } & \{total\_number, is\_work_{n,i} \text{ for } n=1,\ldots,N \text{ and } i=1,\ldots,total\_number\}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'num': [5, 10, 2, 3, 2, 10],
    'n_working_days': 5,
    'n_resting_days': 2
}

#### Problem Data
N = len(data['num'])
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
num_n = data['num']

#### Create a problem instance
problem = pulp.LpProblem("Cafeteria_Staffing_Problem", pulp.LpMinimize)

#### Decision Variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')

is_work = pulp.LpVariable.dicts("is_work",
                                ((n, i) for n in range(N) for i in range(100)), #### 100 is an arbitrary large number of potential employees
                                0, 1, cat='Binary')

#### Objective Function
problem += total_number

#### Constraints
for n in range(N):
    problem += pulp.lpSum(is_work[n, i] for i in range(100)) >= num_n[n]

for i in range(100):
    for n in range(N - n_working_days + 1):
        problem += pulp.lpSum(is_work[n + j, i] for j in range(n_working_days)) <= n_working_days
    for n in range(N - n_working_days - n_resting_days + 1):
        problem += pulp.lpSum(is_work[n + n_working_days + j, i] for j in range(n_resting_days)) == 0

#### Solve the problem
problem.solve()

#### Print the result
print(f'Objective Value: <OBJ>{pulp.value(problem.objective)}</OBJ>')

#### Optimal total number of employees
optimal_total_number = pulp.value(total_number)
print(f"Optimal Total Number of Employees: {optimal_total_number}")

#### Schedule for each employee
for i in range(int(optimal_total_number)):
    schedule = [int(is_work[n, i].varValue) for n in range(N)]
    print(f'Employee {i+1} Schedule: {schedule}')
```

