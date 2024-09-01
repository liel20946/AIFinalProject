import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as mticker
import plotly.express as px

MAX_TIME = 180

def load_results():
    """
    Load the results from the results.csv file.
    :return: results
    """
    sat_results = pd.read_csv('csvs/SAT_results.csv')
    search_results = pd.read_csv('csvs/Search_results.csv')
    return sat_results, search_results

def create_single_search_algo_bar_plot(search_algo_name, total_results):
    """
    Create a bar plot of the search results for a single algorithm.
    :param search_algo_name: name of the search algorithm
    :param total_results: total results of the search algorithms
    """
    # First, select all the results for the search algorithm name
    total_results = total_results[total_results['algorithm'] == search_algo_name]

    mean_times = total_results.groupby('grid size')['time'].mean().reset_index()

    # Use Seaborn to create a bar plot
    plt.figure(figsize=(8, 6))
    ax = sns.barplot(x='grid size', y='time', data=mean_times, palette='viridis')

    # Set the title with some padding
    plt.title(f'Mean Time for {search_algo_name} Solver', pad=20)

    # Set labels with some padding
    plt.xlabel('Grid Size', labelpad=15)
    plt.ylabel('Mean Time (seconds)', labelpad=15)

    # Use a logarithmic scale for the y-axis
    ax.set_yscale("log")

    # Format the y-axis to show regular numbers
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.1f}'))

    # Add solid grid lines on y-axis
    plt.grid(axis='y', linestyle='-')

    # Add the actual value above each bar
    for p in ax.patches:
        height = p.get_height()
        annotation = f'{int(height)}' if height.is_integer() else f'{height:.3f}'

        ax.annotate(annotation,
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 9),
                    textcoords='offset points')

    # Adjust the subplot to add some spacing between plot and title/labels
    plt.subplots_adjust(top=0.85)

    # Save the plot
    plt.savefig(f'{search_algo_name}_results.png')

def create_expended_nodes_bar_plot_for_all_search_algorithms(total_results):
    """
    Create a bar plot of the mean number of expended nodes for all search algorithms.
    :param total_results: total results to plot
    """
    # Group the data by algorithm and grid size and calculate the mean number of expended nodes
    mean_expended_nodes = total_results.groupby(['algorithm', 'grid size'])['expended nodes'].mean().reset_index()

    # Use Seaborn to create a bar plot
    plt.figure(figsize=(12, 8))  # Increase figure size for better readability
    ax = sns.barplot(x='grid size', y='expended nodes', hue='algorithm', data=mean_expended_nodes, palette='mako')

    # Set the title with some padding
    plt.title('Mean Number of Expended Nodes for Search Solvers', pad=20)

    # Set labels with some padding
    plt.xlabel('Grid Size', labelpad=15)
    plt.ylabel('Number of Expended Nodes', labelpad=15)

    # Use a logarithmic scale for the y-axis
    ax.set_yscale("log")

    # Format the y-axis to show regular numbers
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    # Add solid grid lines on y-axis
    plt.grid(axis='y', linestyle='-')

    # Adjust the subplot to add some spacing between plot and title/labels
    plt.subplots_adjust(top=0.85)

    # Save the plot
    plt.savefig('Search_Expended_Nodes_Results.png')

def create_bar_plot_for_all_search_algorithms(total_results):
    """
    Create a bar plot of the mean time for all search algorithms.
    :param total_results: total results of the search algorithms
    """
    # create a bar plot for all search algorithms
    mean_times = total_results.groupby(['algorithm', 'grid size'])['time'].mean().reset_index()

    # Use Seaborn to create a bar plot
    plt.figure(figsize=(12, 8))  # Increase figure size for better readability
    ax = sns.barplot(x='grid size', y='time', hue='algorithm', data=mean_times, palette='viridis')

    # Set the title with some padding
    plt.title('Mean Time for Search Solvers', pad=20)

    # Set labels with some padding
    plt.xlabel('Grid Size', labelpad=15)
    plt.ylabel('Mean Time (seconds)', labelpad=15)

    # Use a logarithmic scale for the y-axis
    ax.set_yscale("log")

    # Format the y-axis to show regular numbers
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.1f}'))

    # Add solid grid lines on y-axis
    plt.grid(axis='y', linestyle='-')

    # Adjust the subplot to add some spacing between plot and title/labels
    plt.subplots_adjust(top=0.85)

    # Save the plot
    plt.savefig('Search_results.png')

def create_expended_nodes_bar_plot(search_algo_name, total_results):
    """
    Create a bar plot of the mean number of expended nodes for a single search algorithm.
    :param search_algo_name: name of the search algorithm
    :param total_results: total results of the search algorithms
    """
    total_results = total_results[total_results['algorithm'] == search_algo_name]
    mean_times = total_results.groupby(['algorithm', 'grid size'])[
        'expended nodes'].mean().reset_index()

    # Use Seaborn to create a bar plot without error bars
    plt.figure(figsize=(12, 8))  # Adjusted figure size for better readability
    ax = sns.barplot(x='grid size', y='expended nodes', data=mean_times,
                     palette='mako', errorbar=None)

    # Set the y-axis to a logarithmic scale
    ax.set_yscale('log')

    # Manually set the ticks on the y-axis
    y_ticks = [1, 10, 100, 1000, 10000, 100000,
               1000000]  # Adjust based on your data range
    ax.set_yticks(y_ticks)

    # Format y-axis to show actual numbers
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    # Add actual numbers above each bar
    for p in ax.patches:
        value = int(p.get_height())
        ax.annotate(f'{value:,}',
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center',
                    xytext=(0, 9),  # 9 points vertical offset
                    textcoords='offset points')

    # Set the title with some padding
    plt.title(f'Mean Number of Expended Nodes for {search_algo_name}', pad=20)

    # Set labels with some padding
    plt.xlabel('Grid Size', labelpad=15)
    plt.ylabel('Number of Expended Nodes', labelpad=15)

    # Adjust the subplot to add some spacing between plot and title/labels
    plt.subplots_adjust(top=0.85)

    # Add solid grid lines on y-axis
    plt.grid(axis='y', linestyle='-')

    # Save the plot
    plt.savefig(f'{search_algo_name}_expended_nodes_result.png')

def create_sat_results_bar_plot(results):
    """
    Create a bar plot of the SAT results.
    :param results: results to plot
    """
    mean_times = results.groupby('grid size')['time'].mean().reset_index()

    # Use Seaborn to create a bar plot
    plt.figure(figsize=(8, 6))
    sns.barplot(x='grid size', y='time', data=mean_times, palette='magma')

    # Set the title with some padding
    plt.title('Mean Time for SAT Solver', pad=20)

    # Set labels with some padding
    plt.xlabel('Grid Size', labelpad=15)
    plt.ylabel('Mean Time (seconds)', labelpad=15)

    # Adjust the subplot to add some spacing between plot and title/labels
    plt.subplots_adjust(top=0.85)

    # Add grid on y-axis
    plt.grid(axis='y')

    # save the plot
    plt.savefig('SAT_results.png')

def clip_time(results):
    """
    Clip the time to the maximum time.
    :param results: results to clip
    :return: clipped results
    """
    # Clip the time to the maximum time
    results['time'] = results['time'].clip(upper=MAX_TIME)
    return results

def create_success_rate_chart(algorithm, search_results):
    """
    Create a chart showing the success and failure rates for a specific algorithm.
    :param algorithm: algorithm to filter the results
    :param search_results: search results to use
    """
    # Filter by the specified algorithm
    search_results = search_results[search_results['algorithm'] == algorithm]

    # Define success and failure based on time (<= 180 is success, > 180 is failure)
    search_results['success'] = search_results['time'] <= 180

    # Calculate the success and failure counts per grid size
    success_failure_by_grid = search_results.groupby(
        ['grid size', 'success']).size().reset_index(name='count')

    # Calculate total count per grid size
    total_by_grid = success_failure_by_grid.groupby('grid size')[
        'count'].sum().reset_index(name='total')

    # Merge total count with success_failure_by_grid to calculate percentages
    success_failure_by_grid = success_failure_by_grid.merge(total_by_grid,
                                                            on='grid size')
    success_failure_by_grid['percentage'] = (success_failure_by_grid['count'] /
                                             success_failure_by_grid[
                                                 'total']) * 100

    # Create a label column to identify success or failure
    success_failure_by_grid['label'] = success_failure_by_grid[
        'success'].apply(lambda x: 'Success' if x else 'Failure')

    # Format the labels for the outer ring
    success_failure_by_grid['outer_label'] = success_failure_by_grid.apply(
        lambda row: f"Grid Size {row['grid size']} ",
        axis=1)

    # Create the sunburst chart using plotly express
    fig = px.sunburst(
        success_failure_by_grid,
        path=['label', 'outer_label'],
        values='count',
        color='label',
        color_discrete_map={'Success': '#63B2FF', 'Failure': '#FF6F61'},
        hover_data={'percentage': ':'}
    )

    # Update the labels for the inner ring
    fig.update_traces(textinfo='label+percent entry',
                      texttemplate='%{label}: %{percentParent}')

    # Update layout to include title with spacing
    fig.update_layout(
        title={
            'text': f"{algorithm}: Success and Failure by Grid Size",
            'x': 0.5,
            'y': 0.95,  # Adjusted to give more space from the top
            'xanchor': 'center',
            'yanchor': 'top',
            'pad': {'b': 10}  # Extra padding to prevent title cut off
        },
        sunburstcolorway=['#63B2FF', '#FF6F61'],
        margin=dict(t=80, l=0, r=0, b=0),  # Added top margin for the title
        uniformtext=dict(minsize=10, mode='hide'),
    )

    fig.write_image(f'{algorithm}_success_failure.png', width=800, height=600)

def create_success_rate_for_all_algorithms(search_results):
    """
    Create a horizontal bar chart showing the success rate for all algorithms.
    :param search_results: search results to use
    """
    # Define success as time <= 180
    search_results['success'] = search_results['time'] <= 180

    # Group by algorithm and calculate success and failure counts
    success_rate = (search_results.groupby('algorithm')['success'].mean() * 100).round(0)
    failure_rate = 100 - success_rate

    # Create a DataFrame for plotting
    plot_df = pd.DataFrame({
        'Algorithm': success_rate.index,
        'Success': success_rate.values,
        'Failure': failure_rate.values
    })

    # Melt the DataFrame to have it in a long format suitable for Plotly Express
    plot_df = plot_df.melt(id_vars=['Algorithm'], value_vars=['Success', 'Failure'],
                           var_name='Outcome', value_name='Percentage')

    # Create the horizontal bar chart with specified colors
    colors = {'Success': 'lightgreen', 'Failure': 'lightcoral'}

    fig = px.bar(plot_df, x='Percentage', y='Algorithm', color='Outcome',
                 orientation='h', text='Percentage',
                 title='Success Rate of Algorithms on Grid Sizes 5-10', color_discrete_map=colors)

    # Center the text on the bars
    fig.update_traces(textposition='inside')

    fig.update_layout(barmode='stack', xaxis=dict(range=[0, 100]))
    fig.write_image('All_Algorithms_Success_Rate.png')

def create_line_graph(search_results, sat_results):
    """
    Create a line graph comparing the time taken by each algorithm and grid size.
    :param search_results: search results
    :param sat_results: SAT results
    """
    # Group the search results by algorithm and grid size and calculate the mean time
    mean_times = search_results.groupby(['algorithm', 'grid size'])['time'].mean().reset_index()

    # Ensure both DataFrames have a common structure
    sat_results['algorithm'] = 'SAT'  # Rename to just SAT for the legend

    # Rename BFS in the search results to BFS (Baseline)
    mean_times['algorithm'] = mean_times['algorithm'].replace('BFS', 'BFS (Baseline)')

    # Merge the sat results with the search results
    merged_results = pd.concat([mean_times, sat_results], axis=0)

    # Create the line graph using plotly express with different markers and line styles
    fig = px.line(
        merged_results,
        x='grid size',
        y='time',
        color='algorithm',
        line_dash='algorithm',  # Use different line styles for each algorithm
        markers=True,           # Add markers to each point
        title='Time Taken by Algorithm and Grid Size'
    )

    # Update the layout to include a title with spacing and other customizations
    fig.update_layout(
        title={
            'text': 'Mean Time for each Algorithm',
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top',
            'pad': {'b': 10}
        },
        margin=dict(t=80, l=0, r=0, b=60),  # Further increase bottom margin
        legend_title_text='Algorithm'  # Change legend title to 'Algorithm'
    )

    # Label x, y axes and ensure y-axis starts slightly below the minimum value
    fig.update_xaxes(title_text='Grid Size')
    fig.update_yaxes(title_text='Mean Time (seconds)', range=[-5, 200], tickvals=[0, 50, 100, 150, 180])

    # Save the line graph
    fig.write_image('All_Algorithms_Line_Graph.png')

def compare_heuristics():
    """
    Compare the number of nodes expanded by different heuristics in the A* algorithm.
    """
    # Read the data into DataFrames
    df_md = pd.read_csv("csvs/A_star_md.csv")
    df_combined = pd.read_csv("csvs/A_star_good_heuristic.csv")

    # Add a column to each DataFrame to indicate the heuristic type
    df_md['Heuristic'] = 'Manhattan Distance Heuristic'
    df_combined['Heuristic'] = 'Combined Heuristic'

    # Concatenate the two DataFrames
    df_combined = pd.concat([df_md, df_combined])

    # Create a line plot comparing the two heuristics
    fig = px.line(df_combined, x='level', y='expended nodes',
                  color='Heuristic', markers=True,
                  labels={
                      "level": "Level",
                      "expended nodes": "Expended Nodes",
                      "Heuristic": "Heuristic"
                  },
                  title="Comparison of Nodes Expanded by Different Heuristics in A* Algorithm")

    # save the plot
    fig.write_image('Heuristic_Comparison.png')
    # fig.show()

def compare_number_of_colors(results):
    """
    Compare the number of expended nodes for different number of colors.
    :param results: results to compare
    """
    # compare the number of expended nodes for different number of colors
    fig = px.line(
        results,
        x="number of colors",
        y="expended nodes",
        title="Number of Expended Nodes in BFS: Different Number of Colors",
        markers=True,
        text="expended nodes"  # Add this line to display values
    )

    # add x, y labels
    fig.update_xaxes(title_text="Number of Colors")
    fig.update_yaxes(title_text="Expended Nodes")

    # Increase the font size for better visibility and position text above
    fig.update_traces(line=dict(width=2), textposition="top center", textfont=dict(size=12))

    fig.write_image('Number_of_Colors_Comparison.png')


def line_graph_success(search_results, sat_results):
    """
    Create a line graph showing the success rate by grid size for each algorithm.

    :param search_results: DataFrame containing search results (with columns 'grid size', 'level', 'time', 'algorithm').
    :param sat_results: DataFrame containing SAT results (with columns 'grid size', 'level', 'time').
    """
    # Merge both datasets into one DataFrame
    sat_results['algorithm'] = 'SAT'
    search_results['algorithm'] = search_results['algorithm'].replace('BFS', 'BFS (Baseline)')
    merged_results = pd.concat(
        [search_results[['grid size', 'level', 'time', 'algorithm']], sat_results], axis=0)

    # Calculate success (1 if time <= 180, else 0)
    merged_results['success'] = (merged_results['time'] < 180).astype(int)

    # Group by grid size and algorithm and calculate the success rate
    success_rate = merged_results.groupby(['grid size', 'algorithm'])['success'].mean().reset_index()
    success_rate['success'] = success_rate['success'] * 100  # Convert to percentage

    # Create the line graph
    fig = px.line(
        success_rate,
        x='grid size',
        y='success',
        color='algorithm',
        line_dash='algorithm',
        markers=True,
        title='Success Rate by Grid Size and Algorithm'
    )

    # Update the layout
    fig.update_layout(
        title={
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top',
            'pad': {'b': 10}
        },
        margin=dict(t=80, l=0, r=0, b=60),
        legend_title_text='Algorithm'
    )

    # Label x, y axes and ensure the graph starts from 5 and ends at 14
    fig.update_xaxes(title_text='Grid Size', tickvals=list(range(5, 15)), range=[5, 14])
    fig.update_yaxes(title_text='Success Rate (%)', range=[-5, 105])  # Extend the Y-axis below 0 and above 100

    # Save the line graph
    fig.write_image('Success_Rate_Line_Graph.png')

    # Show the graph
    fig.show()


if __name__ == "__main__":
    sat_results, search_results = load_results()
    search_results = clip_time(search_results)

    # SAT results
    # create_sat_results_bar_plot(sat_results)

    # Search results

    # runtime
    # create_single_search_algo_bar_plot("BFS", search_results)
    # create_single_search_algo_bar_plot("DFS", search_results)
    # create_single_search_algo_bar_plot("UCS", search_results)
    # create_single_search_algo_bar_plot("A*", search_results)

    # expended nodes
    create_expended_nodes_bar_plot("BFS", search_results)
    # create_expended_nodes_bar_plot("DFS", search_results)
    # create_expended_nodes_bar_plot("UCS", search_results)
    # create_expended_nodes_bar_plot("A*", search_results)
    # create_bar_plot_for_all_search_algorithms(search_results)
    # create_expended_nodes_bar_plot_for_all_search_algorithms(search_results)

    # # compare heuristics
    # compare_heuristics()

    # compare state space
    # base_line_results = pd.read_csv('BaseLineResults.csv')
    # compare_state_space(base_line_results)

    # compare number of colors
    # colors_results = pd.read_csv('number_of_colors_results.csv')
    # compare_number_of_colors(colors_results)

    # success rate
    # create_success_rate_chart("BFS", search_results)
    # create_success_rate_chart("DFS", search_results)
    # create_success_rate_chart("UCS", search_results)
    # create_success_rate_chart("A*", search_results)
    # success rate for all algorithms
    # create_success_rate_for_all_algorithms(search_results)

    # combined results
    # line graph
    # search_results_updated = pd.read_csv('csvs//Search_results_base_and_a_star.csv')
    # search_results_updated = clip_time(search_results_updated)
    # create_line_graph(search_results_updated, sat_results)
    # search_results_for_line_graph = pd.read_csv('csvs/full_results_for_succ.csv')
    # line_graph_success(search_results_for_line_graph, sat_results)








