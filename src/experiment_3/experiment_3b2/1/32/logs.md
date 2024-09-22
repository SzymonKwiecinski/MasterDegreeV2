# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- We suppose that some products can be produced, each of them passing through several stages.
- Necessary time to produce 1 unit of product \var{k} is \var{produce_time_{k, s}} hours for stage \var{s}.
- Availability in working hours is \var{time_{s}} for stage \var{s}. 
- The unitary profits for product \var{k} is \var{profit_{k}}.

INPUT FORMAT:

{
	"produce_time": [[produce_time_{k, s} for s in 1,...,S] for k in 1,...,K],
	"available_time": [time_{s} for s in 1,...,S],
	"profit": [profit_{k} for k in 1,...,K]
}


OBJECTIVE: Determine the quantities to be produced such that all the production constraints are satisfied and the profit is maximized.

OUTPUT INFO:

- \var{quantity} represents the production quantity for each product

OUTPUT FORMAT:

{
	"quantity": [quantity_{k} for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To formulate the given Linear Programming problem in LaTeX, we start by defining the decision variables, constraints, and the objective function that needs to be maximized.

**Decision Variables:**
- Let \( x_k \) represent the quantity to be produced for product \( k \), where \( k = 1, \ldots, K \).

**Objective Function:**
- The objective is to maximize the total profit given by:
  \[
  \text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
  \]

**Constraints:**
- For each stage \( s \), the total production time for all products cannot exceed the available time:
  \[
  \sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot x_k \leq \text{time}_{s}, \quad \text{for } s = 1, \ldots, S
  \]

- Non-negativity constraints for production quantities:
  \[
  x_k \geq 0, \quad \text{for } k = 1, \ldots, K
  \]

Now, let's write this in the LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
\begin{align*}
x_k & : \text{quantity of product } k \text{ to be produced, for } k = 1, \ldots, K
\end{align*}

\subsection*{Objective Function}
\begin{align*}
\text{Maximize } Z & = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\end{align*}

\subsection*{Constraints}
For each stage \( s \):
\begin{align*}
\sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot x_k & \leq \text{time}_{s}, \quad \text{for } s = 1, \ldots, S
\end{align*}

Non-negativity constraints:
\begin{align*}
x_k & \geq 0, \quad \text{for } k = 1, \ldots, K
\end{align*}

\end{document}
```

This LaTeX document outlines the linear programming model for the problem, which includes defining the decision variables, constructing the objective function, and laying out the constraints necessary to determine the optimal production quantities for maximizing profit while adhering to the time constraints at each production stage.

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

\subsection*{Decision Variables}
\begin{align*}
x_k & : \text{quantity of product } k \text{ to be produced, for } k = 1, \ldots, K
\end{align*}

\subsection*{Objective Function}
\begin{align*}
\text{Maximize } Z & = \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\end{align*}

\subsection*{Constraints}
For each stage \( s \):
\begin{align*}
\sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot x_k & \leq \text{time}_{s}, \quad \text{for } s = 1, \ldots, S
\end{align*}

Non-negativity constraints:
\begin{align*}
x_k & \geq 0, \quad \text{for } k = 1, \ldots, K
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data input
data = json.loads('{"NumProducts": 2, "NumMachines": 2, "ProduceTime": [[1, 3], [2, 1]], "AvailableTime": [200, 100], "Profit": [20, 10]}')

K = data['NumProducts']
S = data['NumMachines']
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

#### Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)  #### x_k >= 0

#### Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Total_Profit"

#### Constraints
for s in range(S):
    problem += pulp.lpSum(produce_time[k][s] * x[k] for k in range(K)) <= available_time[s], f"MachineTimeConstraint_{s+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

