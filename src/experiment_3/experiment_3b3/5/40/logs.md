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

\section*{Linear Programming Model for Steel Production}

\textbf{Variables:} \\
Let \( x_k \) be the amount of mineral \( k \) (in tons) that is melted, for \( k = 1, \ldots, K \). \\
Let \( y \) be the amount of Manganese (in tons) added directly.

\textbf{Parameters:} \\
- \( n_{\text{steel\_quant}} \): amount of steel required (tons) \\
- \( mn_{\text{percent}} \): minimum percentage of manganese \\
- \( si_{\text{min}} \): minimum percentage of silicon \\
- \( si_{\text{max}} \): maximum percentage of silicon \\
- \( \text{contsi}_k \): percentage of silicon in mineral \( k \) \\
- \( \text{contmn}_k \): percentage of manganese in mineral \( k \) \\
- \( \text{mang\_price} \): price of manganese (million euros per ton) \\
- \( \text{cost}_k \): cost of mineral \( k \) (million euros per thousand tons) \\
- \( \text{sell\_price} \): selling price of steel (million euros per ton) \\
- \( \text{melt\_price} \): cost of smelting a ton of mineral (million euros) \\

\textbf{Objective:} \\
Maximize profit:

\[
\text{Profit} = n_{\text{steel\_quant}} \cdot \text{sell\_price} - \sum_{k=1}^{K} \left( \frac{\text{cost}_k}{1000} \cdot x_k + \text{melt\_price} \cdot x_k \right) - \text{mang\_price} \cdot y
\]

\textbf{Subject to:}

1. Total steel produced must meet quantity requirement:
\[
\sum_{k=1}^{K} \left( \frac{\text{contsi}_k}{100} \cdot x_k \right) + y \geq n_{\text{steel\_quant}} \cdot \frac{mn_{\text{percent}}}{100}
\]

2. Silicon content must be within specified limits:
\[
si_{\text{min}} \leq \sum_{k=1}^{K} \left( \frac{\text{contsi}_k}{100} \cdot x_k \right) \leq si_{\text{max}}
\]

3. Total steel produced must match the steel quantity required:
\[
\sum_{k=1}^{K} x_k + y = n_{\text{steel\_quant}}
\]

4. Non-negativity constraints:
\[
x_k \geq 0, \quad y \geq 0 \quad \forall k = 1, \ldots, K
\]

\textbf{Output Variables:}
\begin{itemize}
    \item \( \text{amount} = [x_1, x_2, \ldots, x_K] \): amounts of each mineral melted
    \item \( num_{\text{mang}} = y \): amount of Manganese added
\end{itemize}

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

\section*{Linear Programming Model for Steel Production}

\textbf{Variables:} \\
Let \( x_k \) be the amount of mineral \( k \) (in tons) that is melted, for \( k = 1, \ldots, K \). \\
Let \( y \) be the amount of Manganese (in tons) added directly.

\textbf{Parameters:} \\
- \( n_{\text{steel\_quant}} \): amount of steel required (tons) \\
- \( mn_{\text{percent}} \): minimum percentage of manganese \\
- \( si_{\text{min}} \): minimum percentage of silicon \\
- \( si_{\text{max}} \): maximum percentage of silicon \\
- \( \text{contsi}_k \): percentage of silicon in mineral \( k \) \\
- \( \text{contmn}_k \): percentage of manganese in mineral \( k \) \\
- \( \text{mang\_price} \): price of manganese (million euros per ton) \\
- \( \text{cost}_k \): cost of mineral \( k \) (million euros per thousand tons) \\
- \( \text{sell\_price} \): selling price of steel (million euros per ton) \\
- \( \text{melt\_price} \): cost of smelting a ton of mineral (million euros) \\

\textbf{Objective:} \\
Maximize profit:

\[
\text{Profit} = n_{\text{steel\_quant}} \cdot \text{sell\_price} - \sum_{k=1}^{K} \left( \frac{\text{cost}_k}{1000} \cdot x_k + \text{melt\_price} \cdot x_k \right) - \text{mang\_price} \cdot y
\]

\textbf{Subject to:}

1. Total steel produced must meet quantity requirement:
\[
\sum_{k=1}^{K} \left( \frac{\text{contsi}_k}{100} \cdot x_k \right) + y \geq n_{\text{steel\_quant}} \cdot \frac{mn_{\text{percent}}}{100}
\]

2. Silicon content must be within specified limits:
\[
si_{\text{min}} \leq \sum_{k=1}^{K} \left( \frac{\text{contsi}_k}{100} \cdot x_k \right) \leq si_{\text{max}}
\]

3. Total steel produced must match the steel quantity required:
\[
\sum_{k=1}^{K} x_k + y = n_{\text{steel\_quant}}
\]

4. Non-negativity constraints:
\[
x_k \geq 0, \quad y \geq 0 \quad \forall k = 1, \ldots, K
\]

\textbf{Output Variables:}
\begin{itemize}
    \item \( \text{amount} = [x_1, x_2, \ldots, x_K] \): amounts of each mineral melted
    \item \( num_{\text{mang}} = y \): amount of Manganese added
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided in JSON format
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

#### Create the problem
problem = pulp.LpProblem("Steel_Production_Optimization", pulp.LpMaximize)

#### Decision variables
K = len(data['contsi'])
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]
y = pulp.LpVariable('y', lowBound=0, cat='Continuous')

#### Objective function
profit = (
    data['n_steel_quant'] * data['sell_price']
    - pulp.lpSum((data['cost'][k] / 1000 + data['melt_price']) * x[k] for k in range(K))
    - data['mang_price'] * y
)
problem += profit

#### Constraints

#### 1. Total steel produced must meet quantity requirement for manganese
problem += (
    pulp.lpSum((data['contmn'][k] / 100) * x[k] for k in range(K)) + y 
    >= data['n_steel_quant'] * (data['mn_percent'] / 100)
)

#### 2. Silicon content must be within specified limits
problem += (
    data['si_min'] 
    <= pulp.lpSum((data['contsi'][k] / 100) * x[k] for k in range(K))
    <= data['si_max']
)

#### 3. Total steel produced must match the steel quantity required
problem += (
    pulp.lpSum(x[k] for k in range(K)) + y 
    == data['n_steel_quant']
)

#### Solve the problem
problem.solve()

#### Output the results
amount = [pulp.value(x[k]) for k in range(K)]
num_mang = pulp.value(y)
print(f'Amount of each mineral melted: {amount}')
print(f'Amount of Manganese added: {num_mang}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

