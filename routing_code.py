import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

# Routing data for multiple SKUs
routing_data = {
    "SKU 1": {
        "Plant 1": {"DC 1": 22393, "DC 2": 18661, "DC 3": 14928, "DC 4": 0},
        "Plant 2": {"DC 1": 0, "DC 2": 11196, "DC 3": 0, "DC 4": 7464},
    },
    "SKU 2": {
        "Plant 1": {"DC 1": 51959, "DC 2": 60618, "DC 3": 0, "DC 4": 17320},
        "Plant 2": {"DC 1": 0, "DC 2": 8660, "DC 3": 34639, "DC 4": 0},
    },
    "SKU 3": {
        "Plant 1": {"DC 1": 21637, "DC 2": 25243, "DC 3": 0, "DC 4": 7212},
        "Plant 2": {"DC 1": 0, "DC 2": 3606, "DC 3": 14424, "DC 4": 0},
    },
}

# App title
st.title("Real-Time Routing Dashboard")

# Dropdown for SKU selection
selected_sku = st.selectbox("Select an SKU to visualize routing:", options=list(routing_data.keys()))

# Get the data for the selected SKU
data = routing_data[selected_sku]

# Define positions for the graph
positions = {
    "Plant 1": (-1, 0.5),
    "Plant 2": (-1, -0.5),
    "DC 1": (1, 1),
    "DC 2": (1, 0.3),
    "DC 3": (1, -0.3),
    "DC 4": (1, -1),
}

# Create a graph for visualization
G = nx.DiGraph()

# Add nodes
for plant in data.keys():
    G.add_node(plant, type="plant")
for dc in data["Plant 1"].keys():
    G.add_node(dc, type="dc")

# Add edges based on the selected SKU's data
for plant, dcs in data.items():
    for dc, units in dcs.items():
        if units > 0:
            G.add_edge(plant, dc, weight=units)

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))
nx.draw(
    G,
    pos=positions,
    with_labels=True,
    node_color=["gold" if G.nodes[n]["type"] == "plant" else "lightblue" for n in G.nodes],
    node_size=2000,
    edge_color="red",
    arrowsize=20,
    font_size=10,
    font_weight="bold",
    ax=ax
)

# Add edge labels
edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos=positions, edge_labels=edge_labels, font_size=10, ax=ax)

# Display the plot in Streamlit
st.pyplot(fig)
