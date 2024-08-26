import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as mticker

MAX_TIME = 180


def load_results():
    """
    Load the results from the results.csv file.
    :return: results
    """
    sat_results = pd.read_csv('SAT_results.csv')
    search_results = pd.read_csv('Search_results.csv')
    return sat_results, search_results



def create_single_search_algo_bar_plot(search_algo_name, total_results):
    """
    Create a bar plot of the search results for a single algorithm.
    :param search_algo_name: name of the search algorithm
    :param total_results: total results to plot
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
    # Clip the time to the maximum time
    results['time'] = results['time'].clip(upper=MAX_TIME)
    return results

def create_success_rate_graph(results):
    pass


if __name__ == "__main__":
    sat_results, search_results = load_results()
    search_results = clip_time(search_results)

    # SAT results
    # create_sat_results_bar_plot(sat_results)

    # Search results
    create_single_search_algo_bar_plot("BFS", search_results)
    create_single_search_algo_bar_plot("DFS", search_results)
    create_single_search_algo_bar_plot("UCS", search_results)
    create_single_search_algo_bar_plot("A*", search_results)
    create_expended_nodes_bar_plot("BFS", search_results)
    create_expended_nodes_bar_plot("DFS", search_results)
    create_expended_nodes_bar_plot("UCS", search_results)
    create_expended_nodes_bar_plot("A*", search_results)
    create_bar_plot_for_all_search_algorithms(search_results)
    create_expended_nodes_bar_plot_for_all_search_algorithms(search_results)



