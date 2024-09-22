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
To model this problem as a linear programming (LP) problem, we aim to maximize the total profit by determining the optimal production quantities of each product, subject to time constraints at each production stage.

The decision variables are:
- \( x_k \): The quantity of product \( k \) to be produced, for \( k = 1, 2, \ldots, K \).

The objective function, which is to maximize profit, is:
\[ \max \sum_{k=1}^{K} \text{profit}_k \cdot x_k \]

Subject to the constraints:
\[ \sum_{k=1}^{K} \text{produce\_time}_{k, s} \cdot x_k \leq \text{time}_s, \quad \text{for each stage } s = 1, 2, \ldots, S \]
\[ x_k \geq 0, \quad \text{for each product } k = 1, 2, \ldots, K \]

Now, let's write this model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Linear Programming Model:}

\textbf{Objective:}
\[
\max \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{produce\_time}_{k, s} \cdot x_k \leq \text{time}_s, \quad \forall s = 1, 2, \ldots, S
\]
\[
x_k \geq 0, \quad \forall k = 1, 2, \ldots, K
\]

\end{document}
```

This LaTeX code describes the linear programming model for the given problem, where the objective is to maximize the total profit by determining the production quantities of each product subject to stage-wise time constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Linear Programming Model:}

\textbf{Objective:}
\[
\max \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{produce\_time}_{k, s} \cdot x_k \leq \text{time}_s, \quad \forall s = 1, 2, \ldots, S
\]
\[
x_k \geq 0, \quad \forall k = 1, 2, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = '{"NumProducts": 2, "NumMachines": 2, "ProduceTime": [[1, 3], [2, 1]], "AvailableTime": [200, 100], "Profit": [20, 10]}'
parameters = json.loads(data)

#### Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(parameters['NumProducts']), lowBound=0)

#### Objective function
problem += pulp.lpSum(parameters['Profit'][k] * x[k] for k in range(parameters['NumProducts']))

#### Constraints
for s in range(parameters['NumMachines']):
    problem += pulp.lpSum(parameters['ProduceTime'][k][s] * x[k] for k in range(parameters['NumProducts'])) <= parameters['AvailableTime'][s]

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

