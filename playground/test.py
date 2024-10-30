import plotly.graph_objects as go

# Sample data
data1 = {
    'category': ['A', 'B', 'C'],
    'value': [10, 20, 30]
}

data2 = {
    'category': ['A', 'B', 'C'],
    'value': [15, 25, 35]
}

# Create a figure
fig = go.Figure()

# Add the first bar chart (positive values)
fig.add_trace(go.Bar(
    x=data1['value'],
    y=data1['category'],
    orientation='h',
    name='Chart 1',
    marker=dict(color='blue')
))

# Add the second bar chart (negative values for back-to-back effect)
fig.add_trace(go.Bar(
    x=[-val for val in data2['value']],  # Negate the values
    y=data2['category'],
    orientation='h',
    name='Chart 2',
    marker=dict(color='red')
))

# Update layout to control the appearance
fig.update_layout(
    barmode='overlay',
    xaxis=dict(title='Values', tickvals=[-30, -20, -10, 0, 10, 20, 30], ticktext=[30, 20, 10, 0, 10, 20, 30]),
    title='Back-to-Back Bar Charts'
)

