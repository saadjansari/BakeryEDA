import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def make_bar_chart(
    data_frame, x, y, xlabel=None, ylabel=None, title=None, savepath=None
):
    """Make plotly bar chart

    Args:
        data_frame (pd.DataFrame): dataframe with data
        x (str): dataframe column to use for x-axis
        y (str): dataframe column to use for y-axis
        xlabel (str, optional): x-axis label. Defaults to None.
        ylabel (str, optional): y-axis label. Defaults to None.
        title (str, optional): figure title. Defaults to None.

    Returns:
        figure: plotly figure
    """

    fig = px.bar(x=x, y=y, data_frame=data_frame)
    fig.update_xaxes(showgrid=True, ticks="outside", tickson="boundaries")

    if title is not None:
        fig.update_layout(title_text=title)
    if xlabel is not None:
        fig.update_xaxes(title_text=xlabel)
    if ylabel is not None:
        fig.update_yaxes(title_text=ylabel)
    if savepath is not None:
        fig.write_image(savepath)
    return fig


def make_bubble_chart(
    data_frame,
    x,
    y,
    size,
    color,
    xlabel=None,
    ylabel=None,
    title=None,
    ctitle=None,
    savepath=None,
):
    """Make plotly bubble chart

    Args:
        data_frame (pd.DataFrame): dataframe with data
        x (str): dataframe column to use for x-axis
        y (str): dataframe column to use for y-axis
        size (str): dataframe column to use for point size
        color (str): dataframe column to use for point color
        xlabel (str, optional): x-axis label. Defaults to None.
        ylabel (str, optional): y-axis label. Defaults to None.
        title (str, optional): figure title. Defaults to None.
        ctitle (str, optional): color bar title. Defaults to None.

    Returns:
        figure: plotly figure
    """

    fig = px.scatter(x=x, y=y, data_frame=data_frame, size=size, color=color)
    fig.update_xaxes(showgrid=True, ticks="outside", tickson="boundaries")
    fig.update_layout(coloraxis_colorbar=dict(title=ctitle))

    if title is not None:
        fig.update_layout(title_text=title)
    if xlabel is not None:
        fig.update_xaxes(title_text=xlabel)
    if ylabel is not None:
        fig.update_yaxes(title_text=ylabel)
    if savepath is not None:
        fig.write_image(savepath)

    return fig


def make_double_line_plot(
    data_frame, x, y0, y1, ylabel0, ylabel1, xlabel=None, title=None, savepath=None
):
    """Line plot with one or two y-axes

    Args:
        data_frame (pd.DataFrame): dataframe with data
        x (str): dataframe column to use for x-axis
        y0 (str): dataframe column to use for y-axis 0
        y1 (str): dataframe column to use for y-axis 1. 
        ylabel0 (str): y-axis 0 label. 
        ylabel1 (str): y-axis 1 label. 
        xlabel (str, optional): x-axis label. Defaults to None.
        title (str, optional): figure title. Defaults to None.

    Returns:
        figure: plotly figure
    """

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=data_frame[x], y=data_frame[y0], name=ylabel0), secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=data_frame[x], y=data_frame[y1], name=ylabel1), secondary_y=True,
    )

    fig.update_yaxes(title_text=ylabel0, secondary_y=False)
    fig.update_yaxes(title_text=ylabel1, secondary_y=True)
    if title is not None:
        fig.update_layout(title_text=title)
    if xlabel is not None:
        fig.update_xaxes(title_text=xlabel)
    if savepath is not None:
        fig.write_image(savepath)

    return fig
