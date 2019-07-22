"""
    Language Distribution Predictor

    Usage:
        >>> ldp <filename> <sim_length> -d <display_language>

    Params:
        <filename> (str): location of region map json file
        <sim_length> (int): number of cycles
        <display_language> (str): Optionally display chart of language
            distribution

    author: Jacob Lindey
    created: 7-19-2019
    update: 7-20-2019
"""
import click
from simulator import region_map
from visualization import choropleth

@click.command()
@click.argument('file_name')
@click.argument('sim_length', type=int)
@click.option('-d', '--display-language')
def main(file_name, sim_length, display_language):
    """
        Runs Simulation based on json structure and may display a chart.

        Args:
            file_name (str): Location of file containing region map structure.
                Provided by command line args.
            sim_length (int): The number of cycles
            display_language (str): A string arg specifying which language data
                to display in chart. If None no chart is displayed.
    """
    print(f"Running ldp simulation from {file_name} for {sim_length} cycles.")
    if display_language is not None:
        print(f"Displaying {display_language} data in choropleth chart",
                "at 127.0.0.1:60967.")

    # load region data
    map = region_map.RegionMap.from_json(file_name)
    map.load_regions()

    pre_df = map.dataframe  # store pre-sim data

    map.run_sim(sim_length)

    post_df = map.dataframe  # store post-si

    # if user requested a chart display a choropleth
    if display_language is not None:
        try:
            choropleth.show_choropleth(post_df, display_language)
        except ValueError as e:
            print(e)

    print("Pre Simulation Data:")
    print(pre_df)

    print("\nPost Simulation Results:")
    print(post_df)


if __name__ == "__main__":
    main()
