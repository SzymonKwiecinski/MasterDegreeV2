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
To formulate this linear programming problem, we will define the variables, objective function, and constraints based on the provided description.

**Decision Variables:**
- Let \( x_k \) be the quantity of product \( k \) to be produced, for \( k = 1, \ldots, K \).

**Objective Function:**
- Maximize the total profit, which can be represented as:
  \[
  \text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_k \times x_k
  \]

**Constraints:**
- Each stage \( s \) has a limited number of working hours, so the sum of time required to produce the quantities at each stage must not exceed available time:
  \[
  \sum_{k=1}^{K} \text{produce\_time}_{k, s} \times x_k \leq \text{time}_s \quad \text{for each } s = 1, \ldots, S
  \]
- Non-negativity constraints:
  \[
  x_k \geq 0 \quad \text{for each } k = 1, \ldots, K
  \]

The complete mathematical model is as follows:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Product Manufacturing Problem}

\textbf{Decision Variables:}
\begin{align*}
x_k &: \text{Quantity of product } k \text{ to be produced, for } k = 1, \ldots, K
\end{align*}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_k \times x_k
\]

\textbf{Subject to Constraints:}
\begin{align*}
& \sum_{k=1}^{K} \text{produce\_time}_{k, s} \times x_k \leq \text{time}_s, \quad \text{for each } s = 1, \ldots, S \\
& x_k \geq 0, \quad \text{for each } k = 1, \ldots, K
\end{align*}

\end{document}
```

Replace \( \text{profit}_k \), \( \text{produce\_time}_{k, s} \), and \( \text{time}_s \) with their given values in your specific problem instance. This model will help determine the optimal quantities of each product to maximize profit while adhering to the production constraints.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Product Manufacturing Problem}

\textbf{Decision Variables:}
\begin{align*}
x_k &: \text{Quantity of product } k \text{ to be produced, for } k = 1, \ldots, K
\end{align*}

\textbf{Objective Function:}
\[
\text{Maximize } Z = \sum_{k=1}^{K} \text{profit}_k \times x_k
\]

\textbf{Subject to Constraints:}
\begin{align*}
& \sum_{k=1}^{K} \text{produce\_time}_{k, s} \times x_k \leq \text{time}_s, \quad \text{for each } s = 1, \ldots, S \\
& x_k \geq 0, \quad \text{for each } k = 1, \ldots, K
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

K = data['NumProducts']
S = data['NumMachines']
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

#### Create the problem variable
problem = pulp.LpProblem("Product_Manufacturing_Problem", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Total_Profit"

#### Constraints
for s in range(S):
    problem += pulp.lpSum(produce_time[k][s] * x[k] for k in range(K)) <= available_time[s], f"Machine_Constraint_{s+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

