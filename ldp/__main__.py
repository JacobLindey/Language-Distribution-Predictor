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
from data import data_saver
from simulator import region_map
from visualization import choropleth


@click.command()
@click.argument('file_name')
@click.argument('sim_length', type=int)
@click.option('-d', '--display-language')
@click.option('-c', '--console-output/--no-console-output', default=False)
@click.option('-o', '--output-file')
def main(file_name, sim_length, display_language, console_output, output_file):
    """
        Runs Simulation based on json structure and may display a chart.

        Args:
            file_name (str): Location of file containing region map structure.
                Provided by command line args.
            sim_length (int): The number of cycles
            display_language (str): A string arg specifying which language data
                to display in chart. If None no chart is displayed.
    """
    # Print call parameters
    if console_output:
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

    if console_output:
        print("Pre Simulation Data:")
        print(pre_df)

        print("\nPost Simulation Results:")
        print(post_df)

    # if user requested file output, write a file
    if output_file is not None:
        data_saver.export_to_file(output_file, {"Pre-Sim Data":pre_df,
                                              "Post-Sim Data":post_df})

if __name__ == "__main__":
    main()
