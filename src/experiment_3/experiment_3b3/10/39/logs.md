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

\section*{Mathematical Model for Cafeteria Staffing Problem}

\subsection*{Parameters}
\begin{itemize}
    \item \( N \): Total number of days
    \item \( \text{num}_n \): Number of employees required on day \( n \), for \( n = 1, 2, \ldots, N \)
    \item \( d_w \): Number of working days for each employee (i.e., \( n_{\text{working\_days}} \))
    \item \( d_r \): Number of resting days for each employee (i.e., \( n_{\text{resting\_days}} \))
\end{itemize}

\subsection*{Decision Variables}
Let:
\begin{itemize}
    \item \( \text{total\_number} \): Total number of employees to hire
    \item \( x_{n,i} \): A binary variable that is 1 if employee \( i \) works on day \( n \), and 0 otherwise, where \( i = 1, 2, \ldots, \text{total\_number} \)
\end{itemize}

\subsection*{Objective Function}
The objective is to minimize the number of employees hired:
\[
\text{Minimize } \text{total\_number}
\]

\subsection*{Constraints}
1. Ensure the required number of employees for each day \( n \):
\[
\sum_{i=1}^{\text{total\_number}} x_{n,i} \geq \text{num}_n, \quad \forall n = 1, 2, \ldots, N
\]

2. Each employee works for \( d_w \) days and then rests for \( d_r \) days. Define a cycle of \( d_c = d_w + d_r \). The days an employee works influence the days they can take off:
\[
x_{n,i} + x_{n+1,i} + \ldots + x_{n+d_w-1,i} = d_w, \quad \forall n \text{ such that } n + d_w - 1 \leq N
\]
\[
x_{n+d_w,i} + x_{n+d_w+1,i} + \ldots + x_{n+d_c-1,i} = 0, \quad \forall n \text{ such that } n + d_c - 1 \leq N
\]

\subsection*{Output Variables}
The output consists of:
\begin{itemize}
    \item \( \text{total\_number} \): Total number of employees hired.
    \item \( \text{is\_work}_{n,i} \): A 2D array where \( \text{is\_work}_{n,i} \) is 1 if employee \( i \) works on day \( n \), and 0 otherwise.
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

\section*{Mathematical Model for Cafeteria Staffing Problem}

\subsection*{Parameters}
\begin{itemize}
    \item \( N \): Total number of days
    \item \( \text{num}_n \): Number of employees required on day \( n \), for \( n = 1, 2, \ldots, N \)
    \item \( d_w \): Number of working days for each employee (i.e., \( n_{\text{working\_days}} \))
    \item \( d_r \): Number of resting days for each employee (i.e., \( n_{\text{resting\_days}} \))
\end{itemize}

\subsection*{Decision Variables}
Let:
\begin{itemize}
    \item \( \text{total\_number} \): Total number of employees to hire
    \item \( x_{n,i} \): A binary variable that is 1 if employee \( i \) works on day \( n \), and 0 otherwise, where \( i = 1, 2, \ldots, \text{total\_number} \)
\end{itemize}

\subsection*{Objective Function}
The objective is to minimize the number of employees hired:
\[
\text{Minimize } \text{total\_number}
\]

\subsection*{Constraints}
1. Ensure the required number of employees for each day \( n \):
\[
\sum_{i=1}^{\text{total\_number}} x_{n,i} \geq \text{num}_n, \quad \forall n = 1, 2, \ldots, N
\]

2. Each employee works for \( d_w \) days and then rests for \( d_r \) days. Define a cycle of \( d_c = d_w + d_r \). The days an employee works influence the days they can take off:
\[
x_{n,i} + x_{n+1,i} + \ldots + x_{n+d_w-1,i} = d_w, \quad \forall n \text{ such that } n + d_w - 1 \leq N
\]
\[
x_{n+d_w,i} + x_{n+d_w+1,i} + \ldots + x_{n+d_c-1,i} = 0, \quad \forall n \text{ such that } n + d_c - 1 \leq N
\]

\subsection*{Output Variables}
The output consists of:
\begin{itemize}
    \item \( \text{total\_number} \): Total number of employees hired.
    \item \( \text{is\_work}_{n,i} \): A 2D array where \( \text{is\_work}_{n,i} \) is 1 if employee \( i \) works on day \( n \), and 0 otherwise.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
n_days = len(data['num'])
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
d_c = n_working_days + n_resting_days

#### Problem Definition
problem = pulp.LpProblem("Cafeteria_Staffing", pulp.LpMinimize)

#### Decision Variables
total_number = pulp.LpVariable('total_number', lowBound=0, cat='Integer')
#### Binary Decision Variables for each day and each employee
x = pulp.LpVariable.dicts("x", ((n, i) for n in range(n_days) for i in range(100)),
                          cat='Binary')

#### Objective Function
problem += total_number, "Minimize Total Number of Employees"

#### Constraints
for n in range(n_days):
    problem += (pulp.lpSum(x[n, i] for i in range(100)) >= data['num'][n], 
                f"NumEmployees_day{n+1}")

#### Setting up cycle constraints
for n in range(n_days):
    for i in range(100):
        if n + n_working_days <= n_days:
            problem += (pulp.lpSum(x[n + k, i] for k in range(n_working_days)) == n_working_days,
                        f"WorkCycle_start{n+1}_emp{i+1}")
        
        if n + d_c <= n_days:
            problem += (pulp.lpSum(x[n + n_working_days + k, i] for k in range(n_resting_days)) == 0,
                        f"RestCycle_start{n+1}_emp{i+1}")

#### Solve the problem
problem.solve()

#### Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


