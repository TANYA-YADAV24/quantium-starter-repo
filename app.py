import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

df = pd.read_csv("result.csv")
df["date"] = pd.to_datetime(df["date"])

PRICE_INCREASE_DATE = "2021-01-15"

app = Dash(__name__)

app.index_string = """
<!DOCTYPE html>
<html>
<head>
    {%metas%}
    <title>Soul Foods - Pink Morsel Sales</title>
    {%favicon%}
    {%css%}
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #F7F9FC; font-family: 'DM Sans', sans-serif; color: #0A2540; }
        .header { background: #0A2540; padding: 0 48px; display: flex; align-items: center; justify-content: space-between; height: 68px; border-bottom: 3px solid #0070F3; }
        .header-logo { font-family: 'DM Serif Display', serif; font-size: 22px; color: #ffffff; }
        .header-tag { font-size: 12px; color: #94A3B8; letter-spacing: 1.5px; text-transform: uppercase; }
        .main { max-width: 1200px; margin: 0 auto; padding: 40px 32px 60px; }
        .hero { margin-bottom: 36px; }
        .hero h1 { font-family: 'DM Serif Display', serif; font-size: 32px; font-weight: 400; color: #0A2540; margin-bottom: 10px; }
        .hero p { font-size: 15px; color: #64748B; font-weight: 300; max-width: 620px; line-height: 1.6; }
        .controls-row { display: flex; align-items: center; gap: 24px; margin-bottom: 24px; }
        .control-label { font-size: 11px; font-weight: 600; letter-spacing: 1.2px; text-transform: uppercase; color: #64748B; margin-bottom: 6px; }
        .stats-row { display: flex; gap: 20px; margin-bottom: 28px; flex-wrap: wrap; }
        .stat-card { background: #FFFFFF; border: 1px solid #E3E8EF; border-radius: 10px; padding: 18px 28px; flex: 1; min-width: 160px; box-shadow: 0 1px 4px rgba(10,37,64,0.06); }
        .stat-label { font-size: 11px; font-weight: 600; letter-spacing: 1.2px; text-transform: uppercase; color: #64748B; margin-bottom: 6px; }
        .stat-value { font-family: 'DM Serif Display', serif; font-size: 26px; color: #0A2540; }
        .stat-value.up { color: #0070F3; }
        .stat-value.down { color: #E05C2A; }
        .chart-card { background: #FFFFFF; border: 1px solid #E3E8EF; border-radius: 12px; padding: 28px 24px 16px; box-shadow: 0 2px 12px rgba(10,37,64,0.07); }
        .legend-row { display: flex; gap: 24px; margin-top: 14px; padding-left: 8px; }
        .legend-item { display: flex; align-items: center; gap: 8px; font-size: 13px; color: #64748B; }
        .legend-dot { width: 24px; height: 3px; border-radius: 2px; background: #0070F3; }
        .legend-dash { width: 24px; height: 2px; border-top: 2px dashed #E05C2A; }
        .footer { text-align: center; margin-top: 48px; font-size: 12px; color: #94A3B8; }
        .radio-group { display: flex; gap: 8px; flex-wrap: wrap; }
        .radio-label { display: flex; align-items: center; gap: 8px; padding: 8px 18px; border: 1px solid #E3E8EF; border-radius: 8px; font-size: 13px; font-weight: 500; color: #0A2540; cursor: pointer; background: #FFFFFF; user-select: none; }
        .radio-label:hover { border-color: #0070F3; color: #0070F3; background: #F0F7FF; }
        .radio-input { accent-color: #0070F3; width: 15px; height: 15px; cursor: pointer; }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>{%config%}{%scripts%}{%renderer%}</footer>
</body>
</html>
"""

app.layout = html.Div([
    html.Div([
        html.Div("Soul Foods", className="header-logo"),
        html.Div("Sales Intelligence Dashboard", className="header-tag"),
    ], className="header"),

    html.Div([
        html.Div([
            html.H1("Pink Morsel Sales Analysis"),
            html.P("Tracking daily sales performance across all regions to evaluate the impact of the Pink Morsel price increase on 15 January 2021."),
        ], className="hero"),

        html.Div([
            html.Div([
                html.Div("Filter by Region", className="control-label"),
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "South", "value": "south"},
                        {"label": "East", "value": "east"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    className="radio-group",
                    labelClassName="radio-label",
                    inputClassName="radio-input",
                ),
            ]),
        ], className="controls-row"),

        html.Div(id="stat-cards", className="stats-row"),

        html.Div([
            dcc.Graph(id="sales-chart", config={"displayModeBar": False}, style={"height": "460px"}),
            html.Div([
                html.Div([html.Div(className="legend-dot"), html.Span("Daily Sales")], className="legend-item"),
                html.Div([html.Div(className="legend-dash"), html.Span("Price Increase - Jan 15, 2021")], className="legend-item"),
            ], className="legend-row"),
        ], className="chart-card"),

        html.Div("Soul Foods Sales Intelligence - Data through Feb 2022", className="footer"),
    ], className="main"),
])


@app.callback(
    Output("sales-chart", "figure"),
    Output("stat-cards", "children"),
    Input("region-filter", "value"),
)
def update_chart(region):
    filtered = df if region == "all" else df[df["region"] == region]
    daily = filtered.groupby("date", as_index=False)["sales"].sum().sort_values("date")

    before = daily[daily["date"] < PRICE_INCREASE_DATE]["sales"].mean()
    after = daily[daily["date"] >= PRICE_INCREASE_DATE]["sales"].mean()
    change = ((after - before) / before) * 100
    direction = "up" if change >= 0 else "down"

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=daily["date"],
        y=daily["sales"],
        mode="lines",
        line=dict(color="#0070F3", width=2.5),
        name="Daily Sales",
        hovertemplate="<b>%{x|%d %b %Y}</b><br>Sales: <b>%{y:,.0f}</b><extra></extra>",
        fill="tozeroy",
        fillcolor="rgba(0,112,243,0.07)",
    ))

    fig.add_shape(
        type="line",
        x0=PRICE_INCREASE_DATE, x1=PRICE_INCREASE_DATE,
        y0=0, y1=1,
        xref="x", yref="paper",
        line=dict(color="#E05C2A", width=1.5, dash="dash"),
    )

    fig.add_annotation(
        x=PRICE_INCREASE_DATE, y=0.97,
        xref="x", yref="paper",
        text="Price Increase",
        showarrow=False,
        xanchor="left",
        font=dict(size=11, color="#E05C2A", family="DM Sans"),
        bgcolor="rgba(255,255,255,0.85)",
        borderpad=4,
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Total Sales",
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(family="DM Sans, sans-serif", size=13, color="#0A2540"),
        margin=dict(l=56, r=24, t=16, b=56),
        xaxis=dict(showgrid=False, showline=True, linecolor="#E3E8EF", tickfont=dict(size=12, color="#64748B"), title_font=dict(size=12, color="#64748B")),
        yaxis=dict(showgrid=True, gridcolor="#F1F5F9", showline=False, tickfont=dict(size=12, color="#64748B"), title_font=dict(size=12, color="#64748B"), tickformat=","),
        hoverlabel=dict(bgcolor="#0A2540", font_color="#FFFFFF", font_family="DM Sans", font_size=13, bordercolor="#0A2540"),
        showlegend=False,
    )

    cards = [
        html.Div([html.Div("Avg Daily Sales Before", className="stat-label"), html.Div(f"{before:,.0f}", className="stat-value")], className="stat-card"),
        html.Div([html.Div("Avg Daily Sales After", className="stat-label"), html.Div(f"{after:,.0f}", className="stat-value")], className="stat-card"),
        html.Div([html.Div("Change After Price Increase", className="stat-label"), html.Div(f"{'Up' if change >= 0 else 'Down'} {abs(change):.1f}%", className=f"stat-value {direction}")], className="stat-card"),
        html.Div([html.Div("Region", className="stat-label"), html.Div(region.title() if region != "all" else "All Regions", className="stat-value")], className="stat-card"),
    ]

    return fig, cards


if __name__ == "__main__":
    app.run(debug=True)
