"""
    Data structure representing all regions under consideration and their
    connections.

    ldp.simulator.region_map
    ./simulator/region_map.py

    author: Jacob Lindey
    created: 7-19-2019
    update: 7-22-2019
"""
import json
import pandas as pd
from simulator import region


class RegionMap(object):
    """
        Maintains data of and performs transforms on a collection of regions.

        Attributes:
            _regions (Dict, Region): A dict of region.Region objects
                representing each region within the map. Keys are common region
                names in lower_under format.
            _data_dir (str): String specifying the location of a directory
                containing a the data to be loaded into _regions.

    """
    def __init__(self, args: dict):
        self._regions = {}
        for region_name in args["regions"]:
            self._regions[region_name] = region.Region()

        self._data_dir = args["data_dir"]

    def __str__(self) -> str:
        s = ""
        for region in self._regions.values():
            s += f"Name: {region.name}, Population: {region._population} \n"
        return s

    @classmethod
    def from_json(cls, file_name: str):
        """
            Constructs Region Map from json file.

            Pulls data from a json file to create a RegionMap object. See
            'Returns' below for example json structure.

            Args:
                file_name: location of json file

            Returns:
                A RegionMap loaded with data from the specified json file.
                For example, a file regiondata2017.json containing:

                {
                  "data_dir": "./data/region_data_2017",
                  "regions": [
                    "USA",
                    "CAN",
                    "MEX",
                    "OTH"
                  ]
                }

                results in a RegionMap pulling data from ./data/region_data_2017
                and creating the regions "USA", "CAN", "MEX", "OTH".

            Raises:
                FileNotFoundError: an error occured finding the json file in the
                file system
        """
        try:
            file = open(file_name, "r")
            args = json.load(file)
            file.close
        except IOError as e:
            print(e)
            exit()

        return cls(args)

    def load_regions(self):
        """
            Loads region data from _data_dir into _regions.

            The _data_dir directory holds a collection of json files containing
            data for each region. See simulator.region.Region.load_from_json for
            more details on the structure of the json file.
        """
        for region_name, region_obj in self._regions.items():
            region_obj.load_from_json(self._data_dir + "/" + region_name.lower() + ".json")

    def run_sim(self, sim_length):
        """
            Runs the simulation for a number of steps.

            Args:
                sim_length (int): number of steps to run the simulation.
        """
        for i in range(sim_length):
            self._step()

    def _step(self):
        self.grow_populations()
        self.distribute_emigration_requests()
        self.process_immigration_requests()

    def grow_populations(self):
        """
            Increases population of each region.
        """
        for region in self._regions.values():
            region.grow_population()

    def distribute_emigration_requests(self):
        """
            Distributes emigration/immigration requests to destination regions.

            Each region generates a set of emmigration requests each step. This
            method takes those requests and sends them to their destination
            region for processing.

            See region.Region.generate_emigration_requests() for more details on
            emigration request generation.
        """
        for region in self._regions.values():
            requests = region.generate_emigration_requests()
            for request in requests:
                self._regions[request["destination"]].queue_immigration_request(request)

    def process_immigration_requests(self):
        """
            Tells each region to handle its immigration requests in turn.

            Once emmigration requests have been distributed, they must be
            processed.

            See region.process_immigration_queue() for more details.
        """
        for region in self._regions.values():
            region.process_immigration_queue()

    @property
    def dataframe(self) -> pd.DataFrame:
        """
            Returns a pandas.DataFrame of language distribution across regions.
        """
        data = {"regions": list(self._regions.keys())}

        for lang in list(self._regions.values())[0]._lang_dist.keys():
            data[lang] = []

        for region in self._regions.values():
            for lang, dist in region._lang_dist.items():
                data[lang].append(dist)

        return pd.DataFrame(data)
