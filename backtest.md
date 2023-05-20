# Backtest

Keep it simple and stupid backstesting trading strategies.

## Disclamer

_Quod de futuris non est determinata omnino veritas._

## Download data

Soit le cour d'un actif (ici BTC au 15/03/2023 - périodes de 4h):

```
              time     open     high      low    close      volume         count
0   1.664510e+09  19939.0  20055.9  19701.3  19790.4   57.345526  1.137666e+06
1   1.664525e+09  19791.5  19999.0  19789.6  19910.7  138.585049  2.755094e+06
2   1.664539e+09  19915.3  19999.0  19852.0  19938.2  282.864093  5.638161e+06
3   1.664554e+09  19939.4  20575.0  19622.0  20183.5  817.298215  1.633128e+07
4   1.664568e+09  20190.3  20303.0  19900.0  19900.0  200.272247  4.034421e+06
...            ...      ...      ...      ...      ...         ...           ...
995  1.678838e+09  23286.9  23381.5  22300.0  22990.8  432.824320  9.885106e+06
996  1.678853e+09  22940.1  23282.0  22589.6  23048.8  116.567545  2.670718e+06
997  1.678867e+09  22953.5  23116.2  22892.0  23037.4   87.865872  2.021310e+06
998  1.678882e+09  23190.0  23250.0  22903.0  23084.9  373.454050  8.622002e+06
999  1.678896e+09  23394.0  23899.9  23117.5  23374.4  616.774923  1.449521e+07

[1000 rows x 7 columns]
```

<p align="center"><img src="img/bokeh_plot_001.png" /></p>


## Strategy

La stratégie consiste à déterminer selon certains critères établis préalablement, les instants $t_n$ pendant lesquels le marché est favorable à l’achat ($SIG_{buy}(t_n) = 1$) ou à la vente ($SIG_{sell}(t_n) = 1$). Entre le $1^{er}$ signal d’achat et le $1^{er}$ signal de vente suivant, on est en position ($POS(t_n) = 1$).

Stratégie basée sur le RSI.

<p align="center"><img src="img/bokeh_plot_002.png" /></p>

On observe que une période de surachat ($RSI_7 > 70$) augure d'un marché haussier et une zone de survente ($RSI_7 < 30$) un marché baissier.

```python
SIG_buy = RSI_7 > 70
SIG_sell = RSI_7 < 30
```
$SIG_{buy}$:

<p align="center"><img src="img/bokeh_plot_003.png" /></p>

$SIG_{sell}$:

<p align="center"><img src="img/bokeh_plot_004.png" /></p>

$SIG_0 = SIG_{buy} - SIG_{sell}$

<p align="center"><img src="img/bokeh_plot_005.png" /></p>

$POS(t_n) = \begin{cases} SIG_0(t_n) & \text{if } SIG_0(t_n) \ne 0 \\\\ SIG_0(t_{n-1}) & \text{else} \end{cases}$

<p align="center"><img src="img/bokeh_plot_006.png" /></p>

<p align="center"><img src="img/bokeh_plot_007.png" /></p>

## Rendement

Dans l'interval $[t_{n-1}, t_n]$ le rendement vaut:

$$r_0([t_{n-1},t_n]) = { Price(t_n)\over Price(t_{n-1}) }$$

<p align="center"><img src="img/bokeh_plot_010.png" /></p>

Cette définition du rendement est une simplification qui, dans le cadre du développement qui suit, est parfaitement satisfaisante. Petite particularité, le rendement neutre n'est pas 0, le neutre est 1: $Price(t_n) = Price(t_{n-1}) \rightarrow r_0 = 1$.


Interprétation du signal $POS$:

$$\begin{array}{cc|c} POS(t_{n-1}) & POS(t_n) & r_{strat}([t_{n-1},t_n]) \\\\ \hline -1 & -1 & 1 \\\\ -1 & 1 & 1 \\\\ 1 & 1 & r_0([t_{n-1},t_n]) \\\\ 1 & -1 & r_0([t_{n-1},t_n]) \\\\ \end{array}$$

Rendement de la stratégie:

$$r_{strat}(t_n) = \begin{cases} r_0(t_n) & \text{if } POS(t_{n-1}) = 1 \\\\ 1 & \text{else} \end{cases}$$

<p align="center"><img src="img/bokeh_plot_008.png" /></p>

Sans oublier les fees: Lors de chaque transaction (achat et vente), la plateforme prend un fee équivalent à $fee%$:

Même raisonnement que plus haut:

$$r_{fee}(t_n) = \begin{cases} 1-fee & \text{if } POS(t_{n-1}) + POS(t_n) = 1 \\\\ 1 & \text{else} \end{cases}$$

Rendement cumulé:

$$R(t_n) = \prod_{i=1}^{t_n} \biggl( r_{strat}(i) \times r_{fee}(i) \biggr)$$

<p align="center"><img src="img/bokeh_plot_009.png" /></p>
