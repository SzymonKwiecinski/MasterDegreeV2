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

\title{Mathematical Model for Cafeteria Staff Scheduling}
\author{}
\date{}
\maketitle

\section*{Problem Definition}
To operate a cafeteria, the manager must ensure on-call duty based on the statistics on the required staff. The desired number of employees on day \( n \) is denoted as \( num_n \).

\subsection*{Parameters}
\begin{itemize}
    \item \( N \): Total number of days
    \item \( num_n \): Number of desired employees on day \( n \), for \( n = 1, 2, \ldots, N \)
    \item \( n_{working\_days} \): Number of consecutive days each employee works
    \item \( n_{resting\_days} \): Number of days off each employee has
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( total\_number \): Total number of employees to hire
    \item \( is\_work_{n,i} \): A binary variable that indicates if employee \( i \) is working on day \( n \) (1) or resting (0)
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of employees hired:
\[
\text{Minimize } total\_number
\]

\subsection*{Constraints}
1. Ensure that the number of working employees meets the required staff for each day:
\[
\sum_{i=1}^{total\_number} is\_work_{n,i} \geq num_n, \quad \forall n = 1, 2, \ldots, N
\]
2. Each employee has a working and resting cycle:
\[
is\_work_{n,i} = 1 \text{ for } n \in [k \cdot (n_{working\_days} + n_{resting\_days}) + 1, k \cdot (n_{working\_days} + n_{resting\_days}) + n_{working\_days}] \quad \text{for some integer } k
\]
\[
is\_work_{n,i} = 0 \text{ otherwise}
\]
3. Non-negativity constraint on the decision variable:
\[
total\_number \geq 0
\]

\section*{Output}
\begin{itemize}
    \item \( total\_number \): Total number of employees to employ
    \item \( is\_work \): A matrix where \( is\_work_{n,i} \) indicates the working/resting status of employee \( i \) on day \( n \)
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

\title{Mathematical Model for Cafeteria Staff Scheduling}
\author{}
\date{}
\maketitle

\section*{Problem Definition}
To operate a cafeteria, the manager must ensure on-call duty based on the statistics on the required staff. The desired number of employees on day \( n \) is denoted as \( num_n \).

\subsection*{Parameters}
\begin{itemize}
    \item \( N \): Total number of days
    \item \( num_n \): Number of desired employees on day \( n \), for \( n = 1, 2, \ldots, N \)
    \item \( n_{working\_days} \): Number of consecutive days each employee works
    \item \( n_{resting\_days} \): Number of days off each employee has
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( total\_number \): Total number of employees to hire
    \item \( is\_work_{n,i} \): A binary variable that indicates if employee \( i \) is working on day \( n \) (1) or resting (0)
\end{itemize}

\subsection*{Objective Function}
Minimize the total number of employees hired:
\[
\text{Minimize } total\_number
\]

\subsection*{Constraints}
1. Ensure that the number of working employees meets the required staff for each day:
\[
\sum_{i=1}^{total\_number} is\_work_{n,i} \geq num_n, \quad \forall n = 1, 2, \ldots, N
\]
2. Each employee has a working and resting cycle:
\[
is\_work_{n,i} = 1 \text{ for } n \in [k \cdot (n_{working\_days} + n_{resting\_days}) + 1, k \cdot (n_{working\_days} + n_{resting\_days}) + n_{working\_days}] \quad \text{for some integer } k
\]
\[
is\_work_{n,i} = 0 \text{ otherwise}
\]
3. Non-negativity constraint on the decision variable:
\[
total\_number \geq 0
\]

\section*{Output}
\begin{itemize}
    \item \( total\_number \): Total number of employees to employ
    \item \( is\_work \): A matrix where \( is\_work_{n,i} \) indicates the working/resting status of employee \( i \) on day \( n \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON format
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}
num = data['num']
n_working_days = data['n_working_days']
n_resting_days = data['n_resting_days']
N = len(num)

#### Create a linear programming problem
problem = pulp.LpProblem("Cafeteria_Staff_Scheduling", pulp.LpMinimize)

#### Decision variable: total number of employees to hire
total_number = pulp.LpVariable("total_number", lowBound=0, cat='Integer')

#### Decision variables: is_work[n][i] for whether employee i works on day n
is_work = pulp.LpVariable.dicts("is_work", (range(N), range(100)), cat='Binary')  #### Assuming a max of 100 employees

#### Objective Function: Minimize total_number
problem += total_number

#### Constraints to ensure enough staff each day
for n in range(N):
    problem += pulp.lpSum(is_work[n][i] for i in range(100)) >= num[n]

#### Constraints for each employee's working/resting cycle
for i in range(100):
    for k in range((N // (n_working_days + n_resting_days)) + 1):  #### Determine the maximum k
        for j in range(n_working_days):
            day_index = k * (n_working_days + n_resting_days) + j
            if day_index < N:
                problem += is_work[day_index][i] == 1

        for j in range(n_working_days, n_working_days + n_resting_days):
            day_index = k * (n_working_days + n_resting_days) + j
            if day_index < N:
                problem += is_work[day_index][i] == 0

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

