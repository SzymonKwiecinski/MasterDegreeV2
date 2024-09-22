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

\textbf{Variables:}
\begin{itemize}
    \item \( x_k \): Amount of mineral \( k \) melted (in tons), for \( k = 1, 2, \ldots, K \).
    \item \( n_{mang} \): Amount of Manganese added (in tons).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( n_{steel\_quant} \): Total quantity of steel required (in tons).
    \item \( mn_{percent} \): Minimum percentage of Manganese in the steel.
    \item \( si_{min} \): Minimum percentage of Silicon in the steel.
    \item \( si_{max} \): Maximum percentage of Silicon in the steel.
    \item \( contsi_k \): Percentage of Silicon in mineral \( k \).
    \item \( contmn_k \): Percentage of Manganese in mineral \( k \).
    \item \( mang\_price \): Price of Manganese (in million euros per ton).
    \item \( cost_k \): Cost of mineral \( k \) (in million euros per thousand tons).
    \item \( sell\_price \): Selling price of the produced steel (in million euros per ton).
    \item \( melt\_price \): Cost of melting a ton of mineral (in million euros).
\end{itemize}

\textbf{Objective:} Maximize profit, given by

\[
\text{Profit} = (sell\_price \cdot n_{steel\_quant}) - \left( \sum_{k=1}^{K} \left( \frac{cost_k}{1000} \cdot x_k + melt\_price \cdot x_k \right) + mang\_price \cdot n_{mang} \right)
\]

\textbf{Constraints:}
1. Total weight of steel produced:
\[
n_{mang} + \sum_{k=1}^{K} x_k = n_{steel\_quant}
\]

2. Manganese percentage in steel:
\[
\frac{\sum_{k=1}^{K} contmn_k \cdot x_k + n_{mang}}{n_{steel\_quant}} \geq \frac{mn_{percent}}{100}
\]

3. Silicon percentage in steel:
\[
si_{min} \leq \frac{\sum_{k=1}^{K} contsi_k \cdot x_k}{n_{steel\_quant}} \leq si_{max}
\]

4. Non-negativity:
\[
x_k \geq 0, \quad n_{mang} \geq 0 \quad \forall k
\]

\textbf{Output:}
\begin{itemize}
    \item \( amount = [x_1, x_2, \ldots, x_K] \): Amount of each mineral melted.
    \item \( num_{mang} = n_{mang} \): Amount of Manganese directly added.
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

\textbf{Variables:}
\begin{itemize}
    \item \( x_k \): Amount of mineral \( k \) melted (in tons), for \( k = 1, 2, \ldots, K \).
    \item \( n_{mang} \): Amount of Manganese added (in tons).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( n_{steel\_quant} \): Total quantity of steel required (in tons).
    \item \( mn_{percent} \): Minimum percentage of Manganese in the steel.
    \item \( si_{min} \): Minimum percentage of Silicon in the steel.
    \item \( si_{max} \): Maximum percentage of Silicon in the steel.
    \item \( contsi_k \): Percentage of Silicon in mineral \( k \).
    \item \( contmn_k \): Percentage of Manganese in mineral \( k \).
    \item \( mang\_price \): Price of Manganese (in million euros per ton).
    \item \( cost_k \): Cost of mineral \( k \) (in million euros per thousand tons).
    \item \( sell\_price \): Selling price of the produced steel (in million euros per ton).
    \item \( melt\_price \): Cost of melting a ton of mineral (in million euros).
\end{itemize}

\textbf{Objective:} Maximize profit, given by

\[
\text{Profit} = (sell\_price \cdot n_{steel\_quant}) - \left( \sum_{k=1}^{K} \left( \frac{cost_k}{1000} \cdot x_k + melt\_price \cdot x_k \right) + mang\_price \cdot n_{mang} \right)
\]

\textbf{Constraints:}
1. Total weight of steel produced:
\[
n_{mang} + \sum_{k=1}^{K} x_k = n_{steel\_quant}
\]

2. Manganese percentage in steel:
\[
\frac{\sum_{k=1}^{K} contmn_k \cdot x_k + n_{mang}}{n_{steel\_quant}} \geq \frac{mn_{percent}}{100}
\]

3. Silicon percentage in steel:
\[
si_{min} \leq \frac{\sum_{k=1}^{K} contsi_k \cdot x_k}{n_{steel\_quant}} \leq si_{max}
\]

4. Non-negativity:
\[
x_k \geq 0, \quad n_{mang} \geq 0 \quad \forall k
\]

\textbf{Output:}
\begin{itemize}
    \item \( amount = [x_1, x_2, \ldots, x_K] \): Amount of each mineral melted.
    \item \( num_{mang} = n_{mang} \): Amount of Manganese directly added.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'n_steel_quant': 1000, 'mn_percent': 0.45, 'si_min': 3.25, 'si_max': 5.0, 'contsi': [4.0, 1.0, 0.6], 'contmn': [0.45, 0.5, 0.4], 'mang_price': 8.0, 'cost': [21, 25, 15], 'sell_price': 0.45, 'melt_price': 0.005}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided
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

#### Create problem
problem = pulp.LpProblem("Steel_Production_Profit_Maximization", pulp.LpMaximize)

#### Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0) for k in range(len(data['contsi']))]
n_mang = pulp.LpVariable('n_mang', lowBound=0)

#### Objective function
profit = data['sell_price'] * data['n_steel_quant'] \
          - sum((data['cost'][k] / 1000 + data['melt_price']) * x[k] for k in range(len(x))) \
          - data['mang_price'] * n_mang

problem += profit

#### Constraints
#### 1. Total weight of steel produced
problem += n_mang + sum(x) == data['n_steel_quant']

#### 2. Manganese percentage in steel
problem += (sum(data['contmn'][k] * x[k] for k in range(len(x))) + n_mang) >= (data['mn_percent'] / 100) * data['n_steel_quant']

#### 3. Silicon percentage in steel
problem += sum(data['contsi'][k] * x[k] for k in range(len(x))) >= data['si_min'] * data['n_steel_quant']
problem += sum(data['contsi'][k] * x[k] for k in range(len(x))) <= data['si_max'] * data['n_steel_quant']

#### Solve the problem
problem.solve()

#### Output results
amount = [pulp.value(x[k]) for k in range(len(x))]
num_mang = pulp.value(n_mang)

print("Amounts of each mineral melted:", amount)
print("Amount of Manganese directly added:", num_mang)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

