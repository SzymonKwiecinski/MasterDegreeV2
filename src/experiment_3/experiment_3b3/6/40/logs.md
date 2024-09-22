# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A foundry receives a specific order for \var{n_steel_quant} tons of steel. 
- This steel must meet the following characteristics: it must contain at least \var{mn_percent} percentage of manganese (Mn) while its percentage of silicon (SI) must be between \var{si_min} and \var{si_max}.
- To cast this steel, the foundry has limited quantities of several types of minerals.
- The contents expressed in percentage per mineral \var{k} are \var{contsi_{k}} for Si and \var{contmn_{k}} for Mn.
- The process for producing steel is such that direct addition of Mn is possible.
- This Manganese is available at a price of \var{mang_price} million euros per ton. 
- As for the minerals, it costs \var{cost_{k}} million euros per thousand tons for mineral \var{k}.
- The foundry plans to sell the steel produced at \var{sell_price} million euros per ton.
- The cost of smelting a ton of mineral is \var{melt_price} million euros.

INPUT FORMAT:

{
	"n_steel_quant": n_steel_quant,
	"mn_percent": mn_percent,
	"si_min": si_min,
	"si_max": si_max,
	"contsi": [contsi_{k} for k in 1,...,K]
	"contmn": [contmn_{k} for k in 1,...,K]
	"mang_price": mang_price,
	"cost": [cost_{k} for k in 1,...,K]
	"sell_price": sell_price,
	"melt_price": melt_price
}

OBJECTIVE: How should the manufacture manage the steel to maximize profit?

OUTPUT INFO:

- \var{amount} represents the amount of each mineral melted
- \var{num_mang} represents the amount of Manganese directly added

OUTPUT FORMAT:

{
	"amount": [amount_{k} for k in 1,...,K]
	"num_mang": [num_mang]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Linear Programming Model for Steel Production}
\author{}
\date{}
\maketitle

\section*{Problem Definition}

Let:
\begin{itemize}
    \item \( n \) be the required quantity of steel in tons.
    \item \( mn \) be the minimum percentage of manganese required.
    \item \( si_{\text{min}} \) and \( si_{\text{max}} \) be the minimum and maximum percentage of silicon allowed.
    \item \( K \) be the number of different types of minerals available.
    \item \( \text{contsi}_k \) be the percentage of silicon in mineral \( k \).
    \item \( \text{contmn}_k \) be the percentage of manganese in mineral \( k \).
    \item \( \text{mang\_price} \) be the price of manganese in million euros per ton.
    \item \( \text{cost}_k \) be the cost of mineral \( k \) in million euros per thousand tons.
    \item \( \text{sell\_price} \) be the selling price of steel in million euros per ton.
    \item \( \text{melt\_price} \) be the cost of melting a ton of mineral in million euros.
\end{itemize}

\section*{Decision Variables}

Let:
\begin{itemize}
    \item \( x_k \) be the amount of mineral \( k \) melted (in tons).
    \item \( y \) be the amount of manganese added (in tons).
\end{itemize}

\section*{Objective Function}

Maximize profit \( P \):

\[
P = n \cdot \text{sell\_price} - \sum_{k=1}^K \left( \frac{\text{cost}_k}{1000} \cdot x_k \right) - \text{melt\_price} \cdot \sum_{k=1}^K x_k - \text{mang\_price} \cdot y
\]

\section*{Constraints}

1. Total weight of the steel produced:
\[
\sum_{k=1}^K \left( x_k \cdot \frac{\text{contsi}_k}{100} \right) + y \geq n \cdot \frac{mn}{100}
\]

2. Silicon content constraint:
\[
si_{\text{min}} \leq \sum_{k=1}^K \left( x_k \cdot \frac{\text{contsi}_k}{100} \right) \leq si_{\text{max}}
\]

3. Manganese content constraint:
\[
\sum_{k=1}^K \left( x_k \cdot \frac{\text{contmn}_k}{100} \right) + y \geq n \cdot \frac{mn}{100}
\]

4. Non-negativity constraints:
\[
x_k \geq 0 \quad \text{for } k = 1, \ldots, K
\]
\[
y \geq 0
\]

\end{document}
```

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\title{Linear Programming Model for Steel Production}
\author{}
\date{}
\maketitle

\section*{Problem Definition}

Let:
\begin{itemize}
    \item \( n \) be the required quantity of steel in tons.
    \item \( mn \) be the minimum percentage of manganese required.
    \item \( si_{\text{min}} \) and \( si_{\text{max}} \) be the minimum and maximum percentage of silicon allowed.
    \item \( K \) be the number of different types of minerals available.
    \item \( \text{contsi}_k \) be the percentage of silicon in mineral \( k \).
    \item \( \text{contmn}_k \) be the percentage of manganese in mineral \( k \).
    \item \( \text{mang\_price} \) be the price of manganese in million euros per ton.
    \item \( \text{cost}_k \) be the cost of mineral \( k \) in million euros per thousand tons.
    \item \( \text{sell\_price} \) be the selling price of steel in million euros per ton.
    \item \( \text{melt\_price} \) be the cost of melting a ton of mineral in million euros.
\end{itemize}

\section*{Decision Variables}

Let:
\begin{itemize}
    \item \( x_k \) be the amount of mineral \( k \) melted (in tons).
    \item \( y \) be the amount of manganese added (in tons).
\end{itemize}

\section*{Objective Function}

Maximize profit \( P \):

\[
P = n \cdot \text{sell\_price} - \sum_{k=1}^K \left( \frac{\text{cost}_k}{1000} \cdot x_k \right) - \text{melt\_price} \cdot \sum_{k=1}^K x_k - \text{mang\_price} \cdot y
\]

\section*{Constraints}

1. Total weight of the steel produced:
\[
\sum_{k=1}^K \left( x_k \cdot \frac{\text{contsi}_k}{100} \right) + y \geq n \cdot \frac{mn}{100}
\]

2. Silicon content constraint:
\[
si_{\text{min}} \leq \sum_{k=1}^K \left( x_k \cdot \frac{\text{contsi}_k}{100} \right) \leq si_{\text{max}}
\]

3. Manganese content constraint:
\[
\sum_{k=1}^K \left( x_k \cdot \frac{\text{contmn}_k}{100} \right) + y \geq n \cdot \frac{mn}{100}
\]

4. Non-negativity constraints:
\[
x_k \geq 0 \quad \text{for } k = 1, \ldots, K
\]
\[
y \geq 0
\]

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'n_steel_quant': 1000,
    'mn_percent': 0.45,
    'si_min': 3.25,
    'si_max': 5.0,
    'contsi': [4.0, 1.0, 0.6],
    'contmn': [0.45, 0.5, 0.4],
    'mang_price': 8.0,
    'cost': [21, 25, 15],
    'sell_price': 0.45,
    'melt_price': 0.005
}

#### Parameters
n = data['n_steel_quant']
mn = data['mn_percent']
si_min = data['si_min']
si_max = data['si_max']
contsi = data['contsi']
contmn = data['contmn']
mang_price = data['mang_price']
cost = data['cost']
sell_price = data['sell_price']
melt_price = data['melt_price']
K = len(contsi)

#### Problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

#### Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]
y = pulp.LpVariable('y', lowBound=0, cat='Continuous')

#### Objective Function
profit = (n * sell_price -
          pulp.lpSum([(cost[k] / 1000) * x[k] for k in range(K)]) -
          melt_price * pulp.lpSum(x) -
          mang_price * y)

problem += profit

#### Constraints
#### 1. Total weight of steel produced
problem += pulp.lpSum([(x[k] * contsi[k] / 100) for k in range(K)]) + y >= n * mn / 100

#### 2. Silicon content constraint
problem += pulp.lpSum([(x[k] * contsi[k] / 100) for k in range(K)]) >= si_min
problem += pulp.lpSum([(x[k] * contsi[k] / 100) for k in range(K)]) <= si_max

#### 3. Manganese content constraint
problem += pulp.lpSum([(x[k] * contmn[k] / 100) for k in range(K)]) + y >= n * mn / 100

#### Solve
problem.solve()

#### Output
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

