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
To formulate the linear programming problem, let's define the decision variables, objective function, and constraints.

######### Decision Variables
Let \( x_k \) be the quantity of spare part \( k \) to be produced.

######### Objective Function
The objective is to maximize the total profit from producing the spare parts. The profit for each part \( k \) is given by \( \text{profit}_{k} \) and the total profit is the sum of profits from all parts produced:

\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_k \times x_k
\]

######### Constraints
1. **Shop Capacity Constraints:**
   Each shop \( s \) has a limited capacity in terms of worker-hours. The total time spent in shop \( s \) for all parts must not exceed its capacity:

   \[
   \sum_{k=1}^{K} \text{time}_{k, s} \times x_k \leq \text{capacity}_s \quad \text{for each } s = 1, \ldots, S
   \]

2. **Non-negativity Constraints:**
   The quantity of each spare part produced must be non-negative:

   \[
   x_k \geq 0 \quad \text{for each } k = 1, \ldots, K
   \]

Now, let's put this into a LaTeX format.

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Formulation:}

\textbf{Decision Variables:}

Let \( x_k \) be the quantity of spare part \( k \) to be produced.

\textbf{Objective Function:}

Maximize the total profit:

\[
Z = \sum_{k=1}^{K} \text{profit}_k \times x_k
\]

\textbf{Subject to Constraints:}

1. Shop Capacity Constraints:
   \[
   \sum_{k=1}^{K} \text{time}_{k, s} \times x_k \leq \text{capacity}_s, \quad \forall s = 1, \ldots, S
   \]

2. Non-negativity Constraints:
   \[
   x_k \geq 0, \quad \forall k = 1, \ldots, K
   \]

\end{document}
```

This provides a complete formulation of the linear programming problem for the given scenario, aimed at maximizing total profit while respecting the capacity limits of each shop.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Linear Programming Formulation:}

\textbf{Decision Variables:}

Let \( x_k \) be the quantity of spare part \( k \) to be produced.

\textbf{Objective Function:}

Maximize the total profit:

\[
Z = \sum_{k=1}^{K} \text{profit}_k \times x_k
\]

\textbf{Subject to Constraints:}

1. Shop Capacity Constraints:
   \[
   \sum_{k=1}^{K} \text{time}_{k, s} \times x_k \leq \text{capacity}_s, \quad \forall s = 1, \ldots, S
   \]

2. Non-negativity Constraints:
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

#### Extracting data from the JSON format
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

time = data['time']
profit = data['profit']
capacity = data['capacity']

#### Number of spare parts
K = len(profit)

#### Number of shops
S = len(capacity)

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum([profit[k] * x[k] for k in range(K)]), "Total_Profit"

#### Constraints
for s in range(S):
    problem += pulp.lpSum([time[k][s] * x[k] for k in range(K)]) <= capacity[s], f"Capacity_Constraint_Shop_{s}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

