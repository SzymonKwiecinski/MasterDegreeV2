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
To solve this linear programming problem, we need to define the decision variables, the objective function, and the constraints. The decision variables will be the quantities of each product to be produced. The objective is to maximize the total profit, and the constraints are based on the availability of production stages.

Let's denote:
- \( K \) as the number of products.
- \( S \) as the number of stages.
- \( x_k \) as the quantity of product \( k \) to be produced, for \( k = 1, \ldots, K \).

Given:
- \( \text{produce\_time}_{k, s} \) is the time required for producing one unit of product \( k \) at stage \( s \).
- \( \text{time}_s \) is the available working hours for stage \( s \).
- \( \text{profit}_k \) is the profit for one unit of product \( k \).

The mathematical model in LaTeX format is:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\textbf{Linear Programming Model:}

\textbf{Decision Variables:}
\[
x_k \quad \text{for } k = 1, \ldots, K \quad (\text{quantity of product } k)
\]

\textbf{Objective Function:}
Maximize the total profit:
\[
\max \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

\textbf{Constraints:}

For each stage \( s = 1, \ldots, S \), the total production time should not exceed the available time:
\[
\sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot x_k \leq \text{time}_s
\]

Non-negativity constraints for production quantities:
\[
x_k \geq 0 \quad \forall k = 1, \ldots, K
\]

\end{document}
```

This LaTeX code describes the linear programming problem with an objective to maximize the total profit subject to time constraints at each production stage and non-negativity constraints on the decision variables.

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

\textbf{Decision Variables:}
\[
x_k \quad \text{for } k = 1, \ldots, K \quad (\text{quantity of product } k)
\]

\textbf{Objective Function:}
Maximize the total profit:
\[
\max \sum_{k=1}^{K} \text{profit}_k \cdot x_k
\]

\textbf{Constraints:}

For each stage \( s = 1, \ldots, S \), the total production time should not exceed the available time:
\[
\sum_{k=1}^{K} \text{produce\_time}_{k,s} \cdot x_k \leq \text{time}_s
\]

Non-negativity constraints for production quantities:
\[
x_k \geq 0 \quad \forall k = 1, \ldots, K
\]

\end{document}</MATH_MODEL>
<DATA>
{'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

#### Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f"x_{k+1}", lowBound=0, cat='Continuous') for k in range(data['NumProducts'])]

#### Objective function
problem += pulp.lpSum(data['Profit'][k] * x[k] for k in range(data['NumProducts']))

#### Constraints
for s in range(data['NumMachines']):
    problem += pulp.lpSum(data['ProduceTime'][k][s] * x[k] for k in range(data['NumProducts'])) <= data['AvailableTime'][s]

#### Solve the problem
problem.solve()

#### Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

