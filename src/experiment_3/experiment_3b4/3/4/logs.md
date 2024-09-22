# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: MILP

PROBLEM INFO: 
- A hospital wants to make a weekly night shift (12pm-8am) schedule for its nurses. 
- The demand for nurses for the night shift on day \var{j} = 1,...,7 is an integer \var{d_j}. 
- Every nurse works \var{period} days in a row on the night shift, followed by (7 - \var{period}) days off.


INPUT FORMAT: 

{
    "period": period,
    "demand": [d_j for j in 1, ...,7]
}

OBJECTIVE: The goal is to find the minimal number of nurses the hospital needs to hire. 

OUTPUT INFO: 

- for each day \var{j} = 1,...,7, \var{start_j} which shows the number of nurses that start their period on day \var{j}.
- the total number of nurses hired.

OUTPUT FORMAT:

{
    "start": [start_j for j in 1, ...,7],
    "total": total
}


</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To mathematically model this problem, we need to determine the minimum number of nurses required to meet the demand on each of the seven days, considering the constraints of their work periods.

**Model Components:**

- **Decision Variables:**
  - \( x_j \): The number of nurses starting their shift on day \( j \), \( j = 1, \ldots, 7 \).

- **Parameters:**
  - \( d_j \): The demand for nurses on day \( j \).
  - \( \text{period} \): The number of consecutive days a nurse works before getting days off.

- **Constraints:**
  - For each day \( j \), the number of nurses available must meet the demand \( d_j \). 

**Objective:**
Minimize the total number of nurses hired, i.e., \(\sum_{j=1}^{7} x_j\).

Here's how this can be expressed in a mathematical model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model for Scheduling Nurses}

\subsection*{Objective}
Minimize the total number of nurses:
\[
\text{Minimize } \sum_{j=1}^{7} x_j
\]

\subsection*{Constraints}
For each day \( j = 1, \ldots, 7 \), the available nurses should meet or exceed the demand:
\[
\begin{align*}
x_1 + x_7 + x_6 + \cdots + x_{(8-\text{period}) \mod 7} &\geq d_1 \\
x_2 + x_1 + x_7 + \cdots + x_{(9-\text{period}) \mod 7} &\geq d_2 \\
x_3 + x_2 + x_1 + \cdots + x_{(10-\text{period}) \mod 7} &\geq d_3 \\
x_4 + x_3 + x_2 + \cdots + x_{(11-\text{period}) \mod 7} &\geq d_4 \\
x_5 + x_4 + x_3 + \cdots + x_{(12-\text{period}) \mod 7} &\geq d_5 \\
x_6 + x_5 + x_4 + \cdots + x_{(13-\text{period}) \mod 7} &\geq d_6 \\
x_7 + x_6 + x_5 + \cdots + x_{(14-\text{period}) \mod 7} &\geq d_7 \\
\end{align*}
\]

\subsection*{Variables}
\[
x_j \geq 0, \quad \text{integer for } j = 1, \ldots, 7
\]

\end{document}
```

**Explanation:**

- **Objective Function**: We aim to minimize the sum of nurses starting their shift each day.
- **Constraints**: For each day, ensure the sum of nurses working (determined by who started their shift on the current and previous days) meets the demand.
- The modulo operation is used to handle the wrapping of days since we have a weekly schedule.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Mathematical Model for Scheduling Nurses}

\subsection*{Objective}
Minimize the total number of nurses:
\[
\text{Minimize } \sum_{j=1}^{7} x_j
\]

\subsection*{Constraints}
For each day \( j = 1, \ldots, 7 \), the available nurses should meet or exceed the demand:
\[
\begin{align*}
x_1 + x_7 + x_6 + \cdots + x_{(8-\text{period}) \mod 7} &\geq d_1 \\
x_2 + x_1 + x_7 + \cdots + x_{(9-\text{period}) \mod 7} &\geq d_2 \\
x_3 + x_2 + x_1 + \cdots + x_{(10-\text{period}) \mod 7} &\geq d_3 \\
x_4 + x_3 + x_2 + \cdots + x_{(11-\text{period}) \mod 7} &\geq d_4 \\
x_5 + x_4 + x_3 + \cdots + x_{(12-\text{period}) \mod 7} &\geq d_5 \\
x_6 + x_5 + x_4 + \cdots + x_{(13-\text{period}) \mod 7} &\geq d_6 \\
x_7 + x_6 + x_5 + \cdots + x_{(14-\text{period}) \mod 7} &\geq d_7 \\
\end{align*}
\]

\subsection*{Variables}
\[
x_j \geq 0, \quad \text{integer for } j = 1, \ldots, 7
\]

\end{document}</MATH_MODEL>
<DATA>
{'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
Period = data['Period']
demand = data['Demand']

#### Problem
problem = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize)

#### Variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Integer') for j in range(T)]

#### Objective
problem += pulp.lpSum(x[j] for j in range(T)), "Total_Nurses"

#### Constraints
for j in range(T):
    problem += pulp.lpSum(x[(j + i) % T] for i in range(Period)) >= demand[j], f"Demand_Day_{j+1}"

#### Solve
problem.solve()

#### Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

