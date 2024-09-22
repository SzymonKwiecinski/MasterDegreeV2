# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A small firm specializes in making some types of spare automobile parts. 
- Each part is has to go through several shops 
- The required worker-hours for part \var{k} in shop \var{s} is \var{time_{k, s}}.
- The profit of part \var{k} is \var{profit_{k}}.
- The capacity of shop \var{s} is \var{capacity_{s}} working hours.

INPUT FORMAT:

{
	"time": [[time_{k, s} for s in 1,...,S] for k in 1,...,K],
	"profit": [profit_{k} for k in 1,...,K],
	"capacity": [capacity_{s} for s in 1,...,S]
}


OBJECTIVE: Formulate the problem of determining the quantities of each spare part to be made during the month so as to maximize profit.

OUTPUT INFO:

- \var{quantity} represents the amount of each spare part to be made

OUTPUT FORMAT:

{
	"quantity": [quantity_{k} for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To model this problem using linear programming, we need to define decision variables, an objective function, and constraints based on the given data. 

######### Decision Variables
Let \( x_k \) represent the quantity of spare part \( k \) to be produced.

######### Objective Function
We want to maximize the total profit, which is calculated as the sum of the profits for each part multiplied by the quantity produced. Hence, the objective function is:

\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \times x_k
\]

######### Constraints
1. **Capacity Constraints for Each Shop:**
   Each shop \( s \) has a capacity limit in terms of working hours, so the total time spent on different parts in that shop must not exceed its capacity:
   
   \[
   \sum_{k=1}^{K} \text{time}_{k, s} \times x_k \leq \text{capacity}_{s} \quad \text{for each } s = 1, \ldots, S
   \]

2. **Non-negativity Constraints:**
   The quantities of spare parts to be manufactured must be non-negative:

   \[
   x_k \geq 0 \quad \text{for each } k = 1, \ldots, K
   \]

Below is the complete formulation of the problem in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model}

\subsection*{Objective Function}
\begin{align*}
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \times x_k
\end{align*}

\subsection*{Constraints}
\begin{align*}
& \sum_{k=1}^{K} \text{time}_{k, s} \times x_k \leq \text{capacity}_{s} \quad \text{for each } s = 1, \ldots, S \\
& x_k \geq 0 \quad \text{for each } k = 1, \ldots, K
\end{align*}

\end{document}
```

This LaTeX document models the problem as a linear program, defining how to compute the maximum profit while respecting the working hours available in each shop.

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

\subsection*{Objective Function}
\begin{align*}
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \times x_k
\end{align*}

\subsection*{Constraints}
\begin{align*}
& \sum_{k=1}^{K} \text{time}_{k, s} \times x_k \leq \text{capacity}_{s} \quad \text{for each } s = 1, \ldots, S \\
& x_k \geq 0 \quad \text{for each } k = 1, \ldots, K
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Input data
data = json.loads('{"time": [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], "profit": [30, 20, 40, 25, 10], "capacity": [700, 1000]}')

#### Parameters
K = len(data['profit'])  #### Number of items
S = len(data['capacity'])  #### Number of constraints (capacities)
profits = data['profit']
times = data['time']
capacities = data['capacity']

#### Create the 'prob' variable to contain the problem data
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(profits[k] * x[k] for k in range(K)), "Total_Profit"

#### Constraints
for s in range(S):
    problem += pulp.lpSum(times[k][s] * x[k] for k in range(K)) <= capacities[s], f"Capacity_Constraint_{s+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

