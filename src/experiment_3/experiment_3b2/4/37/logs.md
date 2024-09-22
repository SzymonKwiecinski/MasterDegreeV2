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
To formulate the given problem as a Linear Programming (LP) model, we need to define decision variables, an objective function, and constraints based on the information provided.

**Decision Variables:**

Let \( x_k \) represent the quantity of spare part \( k \) to be produced during the month.

**Objective Function:**

The objective is to maximize the total profit, which can be expressed as the sum of the profits from each part multiplied by the quantity produced. Thus, the objective function is:

\[
\text{Maximize } \sum_{k=1}^{K} \text{profit}_{k} \cdot x_k
\]

**Constraints:**

1. For each shop \( s \), the total time spent on all parts should not exceed the shop's capacity. This gives us the set of constraints:

\[
\sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_{s}, \quad \forall s = 1, \ldots, S
\]

2. Non-negativity constraints:

\[
x_k \geq 0, \quad \forall k = 1, \ldots, K
\]

Below is the complete mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model}

\textbf{Decision Variables:}

\[
x_k = \text{Quantity of spare part } k \text{ to be produced}
\]

\textbf{Objective Function:}

Maximize the total profit:

\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot x_k
\]

\textbf{Subject to the constraints:}

1. Capacity constraints for each shop \( s \):

\[
\sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_{s}, \quad \forall s = 1, \ldots, S
\]

2. Non-negativity constraints:

\[
x_k \geq 0, \quad \forall k = 1, \ldots, K
\]

\end{document}
```

This model can be solved using any standard linear programming solver to determine the optimal quantities of each spare part to maximize the total profit while respecting the shop capacities.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model}

\textbf{Decision Variables:}

\[
x_k = \text{Quantity of spare part } k \text{ to be produced}
\]

\textbf{Objective Function:}

Maximize the total profit:

\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_{k} \cdot x_k
\]

\textbf{Subject to the constraints:}

1. Capacity constraints for each shop \( s \):

\[
\sum_{k=1}^{K} \text{time}_{k, s} \cdot x_k \leq \text{capacity}_{s}, \quad \forall s = 1, \ldots, S
\]

2. Non-negativity constraints:

\[
x_k \geq 0, \quad \forall k = 1, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 'profit': [30, 20, 40, 25, 10], 'capacity': [700, 1000]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON format
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

#### Extracting the data
time = data['time']
profit = data['profit']
capacity = data['capacity']

#### Number of spare parts (K) and number of shops (S)
K = len(profit)
S = len(capacity)

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Total_Profit"

#### Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * x[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_{s+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

