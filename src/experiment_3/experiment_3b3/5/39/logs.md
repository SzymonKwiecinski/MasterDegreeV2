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

\section*{Linear Programming Model for Cafeteria Staffing}

\textbf{Variables:}
\begin{itemize}
    \item Let \( x \) denote the total number of employees hired.
    \item Let \( is\_work_{n,i} \) be a binary variable that equals 1 if employee \( i \) is working on day \( n \) and 0 otherwise.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( num_n \): number of employees needed on day \( n \) for \( n = 1, \ldots, N \)
    \item \( n\_working\_days \): number of consecutive working days for each employee.
    \item \( n\_resting\_days \): number of resting days for each employee.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } x
\]

\textbf{Constraints:}
For each day \( n \) (where \( n = 1, \ldots, N \)):
\[
\sum_{i=1}^{x} is\_work_{n,i} \geq num_n \quad \forall n
\]

Each employee works \( n\_working\_days \) followed by \( n\_resting\_days \). Thus, for any employee \( i \),
the following periodic constraints must hold:
\[
is\_work_{n,i} + is\_work_{n+1,i} + \ldots + is\_work_{n+n\_working\_days-1,i} \leq n\_working\_days \quad \forall n \quad \text{where} \ n+n\_working\_days-1 \leq N 
\]

\[
is\_work_{n+n\_working\_days,i} + is\_work_{n+n\_working\_days+1,i} + \ldots + is\_work_{n+n\_working\_days+n\_resting\_days-1,i} = 0 \quad \forall n \quad \text{where} \ n+n\_working\_days+n\_resting\_days-1 \leq N 
\]

\textbf{Output:}
\begin{itemize}
    \item \( total\_number = x \)
    \item \( is\_work \) matrix where \( is\_work_{n,i} \) gives the working status of each employee on each day.
\end{itemize}

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

\section*{Linear Programming Model for Cafeteria Staffing}

\textbf{Variables:}
\begin{itemize}
    \item Let \( x \) denote the total number of employees hired.
    \item Let \( is\_work_{n,i} \) be a binary variable that equals 1 if employee \( i \) is working on day \( n \) and 0 otherwise.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( num_n \): number of employees needed on day \( n \) for \( n = 1, \ldots, N \)
    \item \( n\_working\_days \): number of consecutive working days for each employee.
    \item \( n\_resting\_days \): number of resting days for each employee.
\end{itemize}

\textbf{Objective Function:}
\[
\text{Minimize } x
\]

\textbf{Constraints:}
For each day \( n \) (where \( n = 1, \ldots, N \)):
\[
\sum_{i=1}^{x} is\_work_{n,i} \geq num_n \quad \forall n
\]

Each employee works \( n\_working\_days \) followed by \( n\_resting\_days \). Thus, for any employee \( i \),
the following periodic constraints must hold:
\[
is\_work_{n,i} + is\_work_{n+1,i} + \ldots + is\_work_{n+n\_working\_days-1,i} \leq n\_working\_days \quad \forall n \quad \text{where} \ n+n\_working\_days-1 \leq N 
\]

\[
is\_work_{n+n\_working\_days,i} + is\_work_{n+n\_working\_days+1,i} + \ldots + is\_work_{n+n\_working\_days+n\_resting\_days-1,i} = 0 \quad \forall n \quad \text{where} \ n+n\_working\_days+n\_resting\_days-1 \leq N 
\]

\textbf{Output:}
\begin{itemize}
    \item \( total\_number = x \)
    \item \( is\_work \) matrix where \( is\_work_{n,i} \) gives the working status of each employee on each day.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num_n = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num_n)

#### Problem
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

#### Variables
x = pulp.LpVariable('x', lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts('is_work', ((n, i) for n in range(N) for i in range(N)), cat='Binary')

#### Objective Function
problem += x

#### Constraints
for n in range(N):
    problem += pulp.lpSum(is_work[(n, i)] for i in range(N)) >= num_n[n]

for i in range(N):
    for n in range(N):
        #### Working days constraint
        if n + n_working_days - 1 < N:
            problem += pulp.lpSum(is_work[(n + k, i)] for k in range(n_working_days)) <= n_working_days
        #### Resting days constraint
        if n + n_working_days + n_resting_days - 1 < N:
            problem += pulp.lpSum(is_work[(n + n_working_days + k, i)] for k in range(n_resting_days)) == 0

#### Solve the problem
problem.solve()

#### Display results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
total_number = pulp.value(x)
is_work_status = {(n, i): is_work[(n, i)].varValue for n in range(N) for i in range(N)}

print("Total number of employees hired:", total_number)
print("Working Status Matrix:")
for n in range(N):
    for i in range(N):
        print(f"Day {n} Employee {i}: ", is_work_status[(n, i)])
```


