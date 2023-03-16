# kissbacktest

Keep it simple and stupid backstesting trading strategies.

Download charts from Cryptowatch:

<p align="center"><img src="img/bokeh_plot_001.png" /></p>

Strategy based on $RSI_7$:

<p align="center"><img src="img/bokeh_plot_002.png" /></p>

Buy signal:

$$SIG_{buy} \equiv RSI_7 > 70$$

<p align="center"><img src="img/bokeh_plot_003.png" /></p>

Sell signal:

$$SIG_{sell} \equiv RSI_7 < 30$$

<p align="center"><img src="img/bokeh_plot_004.png" /></p>

Position:

$$SIG_0 \equiv SIG_{buy} - SIG_{sell}$$

<p align="center"><img src="img/bokeh_plot_005.png" /></p>

$$SIG_1(t_n) = \begin{cases} SIG_0(t_n) & \text{if } SIG_0(t_n) \ne 0 \\\\ SIG_0(t_{n-1}) & \text{else} \end{cases}$$

<p align="center"><img src="img/bokeh_plot_006.png" /></p>

$$POS \equiv SIG_1 > 0$$

<p align="center"><img src="img/bokeh_plot_007.png" /></p>

Return if hold:

$$r_0(t_n) = {Price(t_n) \over Price(t_{n-1})}$$

Return strategy:

$$r_{strat}(t_n) = \begin{cases} r_0(t_n) & \text{if } POS(t_{n-1}) = 1 \\\\ 1 & \text{else} \end{cases}$$

fees:

$$r_{fee}(t_n) = \begin{cases} 1-fee & \text{if } POS(t_{n-1}) + POS(t_n) = 1 \\\\ 1 & \text{else} \end{cases}$$

<p align="center"><img src="img/bokeh_plot_008.png" /></p>

Cumulative return:

$$R(t_n) = \prod_{i=1}^{t_n} \biggl( r_{strat}(i) \times r_{fee}(i) \biggr)$$

<p align="center"><img src="img/bokeh_plot_009.png" /></p>
