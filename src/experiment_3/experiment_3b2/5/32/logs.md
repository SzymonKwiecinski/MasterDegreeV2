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
To tackle this problem, we'll create a linear programming model to maximize the profit given the constraints on production times across multiple stages. Let's define the variables, the objective function, and the constraints.

**Variables:**
- Let \( x_k \) be the production quantity for product \( k \).

**Objective Function:**
- Maximize the total profit: \( \sum_{k=1}^{K} \text{profit}_k \times x_k \).

**Constraints:**
- For each stage \( s \), the total time spent on producing all products must not exceed the available time:
  \[
  \sum_{k=1}^{K} \text{produce\_time}_{k,s} \times x_k \leq \text{time}_s \quad \text{for all stages } s
  \]

Now, let's write this model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Sets and Indices:}
\begin{itemize}
    \item \( k \in \{1, \ldots, K\} \): Index for products.
    \item \( s \in \{1, \ldots, S\} \): Index for production stages.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \(\text{produce\_time}_{k, s}\): Time required to produce one unit of product \( k \) at stage \( s \).
    \item \(\text{time}_{s}\): Available working hours at stage \( s \).
    \item \(\text{profit}_{k}\): Unitary profit for product \( k \).
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( x_k \geq 0 \): Quantity of product \( k \) to produce.
\end{itemize}

\textbf{Objective:}
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_k \times x_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{produce\_time}_{k, s} \times x_k \leq \text{time}_s \quad \forall s = 1, \ldots, S
\]

\textbf{Non-negativity:}
\[
x_k \geq 0 \quad \forall k = 1, \ldots, K
\]

\end{document}
```

This model seeks to determine the optimal production quantities \( x_k \) for each product \( k \) such that the total profit is maximized while adhering to the constraints of available working hours at each stage.

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

\textbf{Sets and Indices:}
\begin{itemize}
    \item \( k \in \{1, \ldots, K\} \): Index for products.
    \item \( s \in \{1, \ldots, S\} \): Index for production stages.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \(\text{produce\_time}_{k, s}\): Time required to produce one unit of product \( k \) at stage \( s \).
    \item \(\text{time}_{s}\): Available working hours at stage \( s \).
    \item \(\text{profit}_{k}\): Unitary profit for product \( k \).
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item \( x_k \geq 0 \): Quantity of product \( k \) to produce.
\end{itemize}

\textbf{Objective:}
\[
\text{Maximize} \quad Z = \sum_{k=1}^{K} \text{profit}_k \times x_k
\]

\textbf{Subject to:}
\[
\sum_{k=1}^{K} \text{produce\_time}_{k, s} \times x_k \leq \text{time}_s \quad \forall s = 1, \ldots, S
\]

\textbf{Non-negativity:}
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

#### Data from the JSON format
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

#### Sets and parameters
K = data['NumProducts']
S = data['NumMachines']
produce_time = data['ProduceTime']
available_time = data['AvailableTime']
profit = data['Profit']

#### Create the problem variable
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

#### Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(profit[k] * x[k] for k in range(K)), "Total_Profit"

#### Constraints
for s in range(S):
    problem += pulp.lpSum(produce_time[k][s] * x[k] for k in range(K)) <= available_time[s], f"Time_Constraint_{s+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

