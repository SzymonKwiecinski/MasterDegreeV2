# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- A company produces and sells \var{P} different products. 
- The demand for each product is unlimited, but the company is constrained by cash availability and machine capacity.
- Each unit of the \var{i}-th product requires \var{hour_i} machine hours.
- There are \var{availableHours} machine hours available in the current production period.
- The production costs are \var{cost_i} per unit of the \var{i}-th product.
- The selling prices of the \var{i}-th product is \var{price_i} per unit.
- The available cash is \var{cash}.
- Furthermore, \var{investRate_i} of the sales revenues from the \var{i}-th product will be made available to finance operations during the current period.
- \var{investPercentage_i} is a number between 0 and 1
- The company could increase its available machine hours by \var{upgradeHours}, after spending \var{upgradeCost} for certain repairs. 
- The net income from each product is the revenue we get from selling it minus the production cost and the investment cost.

INPUT FORMAT:

{
    "cash": cash,
    "hour": [hour_i for i in 1, ..., P],
    "cost": [cost_i for i in 1, ..., P],
    "price": [price_i for i in 1, ..., P],
    "investPercentage": [investPercentage_i for i in 1, ..., P],
    "upgradeHours": upgradeHours,   
    "upgradeCost": upgradeCost,
    "availableHours": availableHours,
}

OBJECTIVE: We are aiming at maximizing total net income subject to the cash availability and machine capacity limitations

OUTPUT INFO:

- \var{net_income} shows the net income of the company
- \var{production_i} shows the production quantity of the \var{i}-th product
- \var{upgrade} is a boolean variable that shows whether the company should upgrade its machine capacity or not

OUTPUT FORMAT:

{
    "net_income": net_income,
    "production": [production_i for i in 1, ..., P],
    "upgrade": true/false,
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To formulate this problem as a linear programming model, we need to define the decision variables, objective function, and constraints. Let's declare the decision variables as follows:

1. \( x_i \): the number of units of the \( i \)-th product to be produced.
2. \( u \): a binary variable indicating whether the company should upgrade its machine capacity (1 for upgrade, 0 for no upgrade).

The objective is to maximize the total net income, which can be expressed as:

\[
\text{Net Income} = \sum_{i=1}^{P} \left( \text{price}_i \times x_i - \text{cost}_i \times x_i - \text{investPercentage}_i \times \text{price}_i \times x_i \right) - \text{upgradeCost} \times u
\]

Subject to the following constraints:

1. Machine capacity constraint:
   \[
   \sum_{i=1}^{P} \text{hour}_i \times x_i \leq \text{availableHours} + u \times \text{upgradeHours}
   \]

2. Cash constraint:
   \[
   \sum_{i=1}^{P} \text{cost}_i \times x_i \leq \text{cash} + \sum_{i=1}^{P} \text{investPercentage}_i \times \text{price}_i \times x_i
   \]

3. Non-negativity:
   \[
   x_i \geq 0 \quad \text{for all } i
   \]
   \[
   u \in \{0, 1\}
   \]

Now, let's represent the model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\subsection*{Decision Variables}
\begin{align*}
x_i & : \text{Number of units of product } i \text{ to be produced} \\
u & : \text{Binary variable indicating whether to upgrade machine capacity}
\end{align*}

\subsection*{Objective Function}
Maximize the total net income:
\begin{equation*}
\text{Maximize } \sum_{i=1}^{P} \left( \text{price}_i \times x_i - \text{cost}_i \times x_i - \text{investPercentage}_i \times \text{price}_i \times x_i \right) - \text{upgradeCost} \times u
\end{equation*}

\subsection*{Constraints}
\begin{align*}
\text{Machine Capacity: } & \sum_{i=1}^{P} \text{hour}_i \times x_i \leq \text{availableHours} + u \times \text{upgradeHours} \\
\text{Cash Constraint: } & \sum_{i=1}^{P} \text{cost}_i \times x_i \leq \text{cash} + \sum_{i=1}^{P} \text{investPercentage}_i \times \text{price}_i \times x_i \\
\text{Non-negativity: } & x_i \geq 0 \quad \text{for all } i \\
\text{Binary Constraint: } & u \in \{0, 1\}
\end{align*}

\end{document}
```

This structured model captures the objective of maximizing net income while adhering to the available cash and machine capacity constraints. The variable \( u \) decides whether investing in machine upgrades is beneficial under the given constraints.

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
x_i & : \text{Number of units of product } i \text{ to be produced} \\
u & : \text{Binary variable indicating whether to upgrade machine capacity}
\end{align*}

\subsection*{Objective Function}
Maximize the total net income:
\begin{equation*}
\text{Maximize } \sum_{i=1}^{P} \left( \text{price}_i \times x_i - \text{cost}_i \times x_i - \text{investPercentage}_i \times \text{price}_i \times x_i \right) - \text{upgradeCost} \times u
\end{equation*}

\subsection*{Constraints}
\begin{align*}
\text{Machine Capacity: } & \sum_{i=1}^{P} \text{hour}_i \times x_i \leq \text{availableHours} + u \times \text{upgradeHours} \\
\text{Cash Constraint: } & \sum_{i=1}^{P} \text{cost}_i \times x_i \leq \text{cash} + \sum_{i=1}^{P} \text{investPercentage}_i \times \text{price}_i \times x_i \\
\text{Non-negativity: } & x_i \geq 0 \quad \text{for all } i \\
\text{Binary Constraint: } & u \in \{0, 1\}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'P': 2, 'Cash': 3000, 'Hour': [2, 6], 'Cost': [3, 2], 'Price': [6, 5], 'InvestPercentage': [0.4, 0.3], 'UpgradeHours': 2000, 'UpgradeCost': 400, 'AvailableHours': 2000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Given data
data = {
    'P': 2,
    'Cash': 3000,
    'Hour': [2, 6],
    'Cost': [3, 2],
    'Price': [6, 5],
    'InvestPercentage': [0.4, 0.3],
    'UpgradeHours': 2000,
    'UpgradeCost': 400,
    'AvailableHours': 2000
}

#### Create the problem
problem = pulp.LpProblem("Maximize_Net_Income", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(data['P'])]
u = pulp.LpVariable('u', cat='Binary')

#### Objective Function
profit_terms = [data['Price'][i] * x[i] - data['Cost'][i] * x[i] - data['InvestPercentage'][i] * data['Price'][i] * x[i] for i in range(data['P'])]
objective = pulp.lpSum(profit_terms) - data['UpgradeCost'] * u
problem += objective

#### Constraints
#### Machine Capacity Constraint
problem += pulp.lpSum(data['Hour'][i] * x[i] for i in range(data['P'])) <= data['AvailableHours'] + u * data['UpgradeHours']

#### Cash Constraint
problem += pulp.lpSum(data['Cost'][i] * x[i] for i in range(data['P'])) <= data['Cash'] + pulp.lpSum(data['InvestPercentage'][i] * data['Price'][i] * x[i] for i in range(data['P']))

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

