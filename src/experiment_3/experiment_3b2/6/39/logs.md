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
To formulate the given problem as a Linear Programming (LP) problem, we need to model the scheduling of employees over a series of days such that the minimum number of employees is hired while satisfying the work and rest requirements.

Let's define the decision variables, constraints, and objective function:

**Decision Variables:**
- Let \( x_i \) be a binary variable representing whether employee \( i \) is hired or not.
- Let \( y_{n,i} \) be a binary variable representing whether employee \( i \) is working on day \( n \).

**Parameters:**
- \( \text{num}_n \): Number of employees required on day \( n \).
- \( \text{n\_working\_days} \): Number of consecutive days each employee works.
- \( \text{n\_resting\_days} \): Number of consecutive days each employee rests.

**Objective Function:**
Minimize the total number of employees hired:

\[
\text{minimize} \quad \sum_{i=1}^{I} x_i
\]

**Constraints:**
1. Satisfy the required number of employees on each day \( n \):

\[
\sum_{i=1}^{I} y_{n,i} \geq \text{num}_n, \quad \forall n
\]

2. Ensure that each employee works for \text{n\_working\_days} followed by \text{n\_resting\_days}:

For each employee \( i \), for every sequence of \text{n\_working\_days} \(\to\) \text{n\_resting\_days}, the employee can either work or rest:

\[
y_{n,i} \leq x_i, \quad \forall n, \forall i
\]

- This constraint ensures that an employee \( i \) can only work if they are hired.

Now, we'll translate this problem into a LaTeX formatted mathematical model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Decision Variables}
\begin{align*}
x_i & : \text{Binary variable indicating if employee } i \text{ is hired}, \quad \forall i = 1, \ldots, I\\
y_{n,i} & : \text{Binary variable indicating if employee } i \text{ works on day } n, \quad \forall n, \forall i
\end{align*}

\subsection*{Objective Function}
Minimize the total number of employees:
\[
\text{minimize} \quad \sum_{i=1}^{I} x_i
\]

\subsection*{Constraints}
\begin{align*}
& \text{1. Employee requirement per day:}\\
& \sum_{i=1}^{I} y_{n,i} \geq \text{num}_n, \quad \forall n\\
& \text{2. Employee working days:}\\
& y_{n,i} \leq x_i, \quad \forall n, \forall i\\
\end{align*}

\subsection*{Additional Notes}
- Each employee works for \text{n\_working\_days} followed by \text{n\_resting\_days}.
- The planning must ensure that these cycles are respected.
- The decision variables \( x_i \) and \( y_{n,i} \) are binary.

\end{document}
```

This mathematical model is structured to minimize the total number of employees while ensuring daily staffing requirements are met considering the working and resting cycle.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Decision Variables}
\begin{align*}
x_i & : \text{Binary variable indicating if employee } i \text{ is hired}, \quad \forall i = 1, \ldots, I\\
y_{n,i} & : \text{Binary variable indicating if employee } i \text{ works on day } n, \quad \forall n, \forall i
\end{align*}

\subsection*{Objective Function}
Minimize the total number of employees:
\[
\text{minimize} \quad \sum_{i=1}^{I} x_i
\]

\subsection*{Constraints}
\begin{align*}
& \text{1. Employee requirement per day:}\\
& \sum_{i=1}^{I} y_{n,i} \geq \text{num}_n, \quad \forall n\\
& \text{2. Employee working days:}\\
& y_{n,i} \leq x_i, \quad \forall n, \forall i\\
\end{align*}

\subsection*{Additional Notes}
- Each employee works for \text{n\_working\_days} followed by \text{n\_resting\_days}.
- The planning must ensure that these cycles are respected.
- The decision variables \( x_i \) and \( y_{n,i} \) are binary.

\end{document}</MATH_MODEL>
<DATA>
{'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON input
data = {'num': [5, 10, 2, 3, 2, 10], 'n_working_days': 5, 'n_resting_days': 2}

#### Parameters
num_days = len(data['num'])
I = 10  #### Assume a maximum of 10 employees for the model

#### Create the linear programming problem
problem = pulp.LpProblem("Employee_Scheduling_Problem", pulp.LpMinimize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(I), cat='Binary')  #### Employee hired
y = pulp.LpVariable.dicts("y", (range(num_days), range(I)), cat='Binary')  #### Employee working on day n

#### Objective Function: Minimize the total number of employees hired
problem += pulp.lpSum(x[i] for i in range(I)), "Minimize_Employees"

#### Constraints

#### Employee requirement per day
for n in range(num_days):
    problem += pulp.lpSum(y[n][i] for i in range(I)) >= data['num'][n], f"Employee_Requirement_Day_{n}"

#### Employee working days
for n in range(num_days):
    for i in range(I):
        problem += y[n][i] <= x[i], f"Working_Days_Employee_{i}_Day_{n}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

