import pandas as pd
from dash import Dash, dcc, html
import plotly.graph_objects as go

df = pd.read_csv("result.csv")
df["date"] = pd.to_datetime(df["date"])
daily = df.groupby("date", as_index=False)["sales"].sum().sort_values("date")

PRICE_INCREASE_DATE = "2021-01-15"

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=daily["date"],
    y=daily["sales"],
    mode="lines",
    line=dict(color="#E05C2A", width=2),
    name="Total Sales"
))

fig.add_shape(
    type="line",
    x0=PRICE_INCREASE_DATE,
    x1=PRICE_INCREASE_DATE,
    y0=0,
    y1=1,
    xref="x",
    yref="paper",
    line=dict(color="#444", width=1.5, dash="dash")
)

fig.add_annotation(
    x=PRICE_INCREASE_DATE,
    y=1,
    xref="x",
    yref="paper",
    text="Price Increase (Jan 15, 2021)",
    showarrow=False,
    xanchor="left",
    yanchor="top",
    font=dict(size=12, color="#444"),
    bgcolor="rgba(255,255,255,0.7)"
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Total Sales",
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Arial, sans-serif", size=13),
    margin=dict(l=60, r=40, t=30, b=60),
    xaxis=dict(showgrid=True, gridcolor="#eee"),
    yaxis=dict(showgrid=True, gridcolor="#eee"),
    legend=dict(orientation="h", y=-0.15)
)

app = Dash(__name__)

app.layout = html.Div([
    html.H1(
        "Pink Morsel Sales — Before & After the Price Increase",
        style={"textAlign": "center", "fontFamily": "Arial, sans-serif", "color": "#222", "padding": "24px 16px 8px"}
    ),
    html.P(
        "Daily total sales across all regions. The dashed line marks the Pink Morsel price increase on 15 January 2021.",
        style={"textAlign": "center", "fontFamily": "Arial, sans-serif", "color": "#666", "marginBottom": "8px"}
    ),
    dcc.Graph(
        figure=fig,
        style={"height": "520px", "maxWidth": "1100px", "margin": "0 auto"}
    )
], style={"backgroundColor": "white", "minHeight": "100vh"})

if __name__ == "__main__":
    app.run(debug=True)
