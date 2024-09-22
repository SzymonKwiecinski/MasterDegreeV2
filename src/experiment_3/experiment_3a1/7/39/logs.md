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

\section*{Mathematical Model for Employee Scheduling in Cafeteria}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( N \) be the total number of days.
    \item Let \( num_n \) be the number of employees required on day \( n \) where \( n = 1, 2, \ldots, N \).
    \item Let \( n_{working} \) be the number of consecutive working days for each employee.
    \item Let \( n_{resting} \) be the number of consecutive resting days for each employee.
    \item Let \( T = n_{working} + n_{resting} \) be the total cycle length for each employee.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( total\_number \) be the total number of employees hired.
    \item Let \( is\_work_{n,i} \) be a binary variable that equals 1 if employee \( i \) is working on day \( n \) and 0 otherwise, where \( i = 1, 2, \ldots, total\_number \) and \( n = 1, 2, \ldots, N \).
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of employees hired:
\[
\text{Minimize } total\_number
\]

\subsection*{Constraints}
\begin{enumerate}
    \item For each day \( n \), the total number of employees working must meet the requirement:
    \[
    \sum_{i=1}^{total\_number} is\_work_{n,i} \geq num_n \quad \forall n = 1, 2, \ldots, N
    \]
    
    \item Each employee must follow their working and resting cycle. For each employee \( i \):
    \[
    is\_work_{n,i} = 
    \begin{cases}
      1, & \text{for } n \mod T < n_{working} \\
      0, & \text{for } n \mod T \geq n_{working}
    \end{cases} \quad \forall n = 1, 2, \ldots, N
    \]
    
\end{enumerate}

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

\section*{Mathematical Model for Employee Scheduling in Cafeteria}

\subsection*{Parameters}
\begin{itemize}
    \item Let \( N \) be the total number of days.
    \item Let \( num_n \) be the number of employees required on day \( n \) where \( n = 1, 2, \ldots, N \).
    \item Let \( n_{working} \) be the number of consecutive working days for each employee.
    \item Let \( n_{resting} \) be the number of consecutive resting days for each employee.
    \item Let \( T = n_{working} + n_{resting} \) be the total cycle length for each employee.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item Let \( total\_number \) be the total number of employees hired.
    \item Let \( is\_work_{n,i} \) be a binary variable that equals 1 if employee \( i \) is working on day \( n \) and 0 otherwise, where \( i = 1, 2, \ldots, total\_number \) and \( n = 1, 2, \ldots, N \).
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of employees hired:
\[
\text{Minimize } total\_number
\]

\subsection*{Constraints}
\begin{enumerate}
    \item For each day \( n \), the total number of employees working must meet the requirement:
    \[
    \sum_{i=1}^{total\_number} is\_work_{n,i} \geq num_n \quad \forall n = 1, 2, \ldots, N
    \]
    
    \item Each employee must follow their working and resting cycle. For each employee \( i \):
    \[
    is\_work_{n,i} = 
    \begin{cases}
      1, & \text{for } n \mod T < n_{working} \\
      0, & \text{for } n \mod T \geq n_{working}
    \end{cases} \quad \forall n = 1, 2, \ldots, N
    \]
    
\end{enumerate}

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
Here is the Python script using the Pulp library based on the provided mathematical model and data:

```python
import pulp

#### Data from the provided JSON format
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num_n = data['num']
n_working = data['n_working_days']
n_resting = data['n_resting_days']
N = len(num_n)
T = n_working + n_resting

#### Create the problem
problem = pulp.LpProblem("Employee_Scheduling", pulp.LpMinimize)

#### Decision Variables
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(total_number)), cat='Binary')

#### Objective Function: Minimize the total number of employees hired
problem += total_number, "Minimize_Employees"

#### Constraints
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(total_number)) >= num_n[n], f"Requirement_Day_{n+1}"

for i in range(total_number):
    for n in range(N):
        if n % T < n_working:
            problem += is_work[n][i] == 1, f"Working_Employee_{i+1}_Day_{n+1}"
        else:
            problem += is_work[n][i] == 0, f"Resting_Employee_{i+1}_Day_{n+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

This Python script sets up the linear programming model for employee scheduling in a cafeteria using the Pulp library. It includes data parsing, decision variable definitions, constraint implementations, and finally, it solves the problem and prints the objective value as required.

