"""
    Data structure representing a region within a RegionMap.

    Typically represents a continent or nation. Handles population growth,
    immigration/emigration, interal pressures.

    ldp.simulator.region
    ./simulator/region.py

    author: Jacob Lindey
    created: 7-19-2019
    update: 7-22-2019
"""
import json


class Region(object):
    """
        Maintains data and performs transforms for a region in a RegionMap.

        Attributes:
            name (str): Name of region. lower_under format.
            _population (float): Population of region in millions of persons.
            _births_per_mil (float): Birth rate in millions of birth per year.
            _deaths_per_mil (float): Death rate in millions of deaths per year.
            _emigration_rate (float): Emigration rate from region to all other
                regions each year. Recorded as percentage of total population.
            _lang_dist (Dict, float): A dict of floats each representing the
                proportion of individuals within the region that speak a
                language fluently as a first, second, or third language. These
                proportions DO NOT sum to 100%, i.e. a person can speak more
                than one language. Keys take the form of language names as
                lower_under strings.
            _regional_rates (Dict, floats): A dict of floast each representing
                the proportion of individuals that emigrated from the region in
                a given year that will end at a particular destination region.
                Keys take the form of region names as lower_under strings.
            _immigration_queue (list, Dict):  A list of dicts containing
                requests for population transfer between regions. The list is
                initialized empty.
    """
    def __init__(self):
        self.name = None
        self._population = None
        self._births_per_mil = None
        self._deaths_per_mil = None
        self._emigration_rate = None
        self._lang_dist = {}
        self._regional_rates = {}
        self._immigration_queue = []

    def __str__(self) -> str:
        s = ""
        s += self.name.upper() + '\n'
        s += f"Population:      {self._population} \n"
        s += f"Births/Million:  {self._births_per_mil} \n"
        s += f"Deaths/Million:  {self._deaths_per_mil} \n"

        s += "Language Distribution: \n"
        for lang, dist in self._lang_dist.items():
            s += "  " + lang + ": " + str(dist) + "\n"

        s += f"Emigration Rate: {self._emigration_rate} \n"
        for region, rate in self._regional_rates.items():
            s += "  " + region + ": " + str(rate) + "\n"

        return s

    def load_from_json(self, file_name: str):
        """
            Loads data from json file into self.

            The json files take the following form:

                {
                  "name": "USA",
                  "population": 327.2,
                  "births_per_mil": 0.012500,
                  "deaths_per_mil": 0.008200,
                  "lang_dist": {
                      "english": 0.702,
                      "spanish": 0.123,
                      "french": 0.003,
                      "chinese": 0.01
                  },
                  "emigration_rate": 0.01,
                  "regional_rates": {
                    "USA": 0,
                    "MEX": 0.10,
                    "CAN": 0.80,
                    "OTH": 0.10
                  }
                }

            Each file for a given map definition needs to have the same set
            of considered languages under lang_dist and destinations in
            regional_rates.

            Args:
                file_name (str): name of the json file with directory and
                    extension.

            Raises:
                FileNotfoundError: the file could not be found at the specified
                    location.
        """
        try:
            file = open(file_name, "r")
            args = json.load(file)
        except FileNotFoundError:
            print(f"FileNotFoundError: The file {file_name} specified in the",
                    "region data file does not exist.")
            exit()
        file.close()

        self.name = args["name"]
        self._population = args["population"]
        self._births_per_mil = args["births_per_mil"]
        self._deaths_per_mil = args["deaths_per_mil"]
        self._emigration_rate = args["emigration_rate"]

        self._lang_dist = {}
        for lang, dist in args["lang_dist"].items():
            self._lang_dist[lang] = dist

        self._regional_rates = {}
        for region, rate in args["regional_rates"].items():
            self._regional_rates[region] = rate

    def grow_population(self):
        """Increases populaiton according to birth and death rates."""
        # find net population growth
        net_growth = ((self._births_per_mil - self._deaths_per_mil)
                        * self._population)

        # increase population
        self._population += net_growth

    def generate_emigration_requests(self):
        """
            Returns a list of emigration requests to be processed by other
            regions. A dict is used to represent the emigration requests.
        """
        requests = []

        # find emigrating population
        emigrating_pop = self._emigration_rate * self._population

        # distribute to destinations
        for region, rate in self._regional_rates.items():
            requests.append({   "destination": region,
                                "population": emigrating_pop * rate,
                                "lang_dist": self._lang_dist })

        return requests

    def queue_immigration_request(self, request):
        """
            Queue an immigration request to be processed when
            process_immigration_queue() is called.
        """
        self._immigration_queue.append(request)

    def _process_immigration_request(self, request):
        """
            Processes a single immigration request. Internal use only.

            Args:
                request (dict): A dictionary of the form:
                        {
                            "destination": Region,
                            "population": int,
                            "lang_dist": float
                        }
                    used to represent the population moving into the region.
        """
        new_population = self._population + request["population"]

        # performs a weighted average on the distrubtion after mixing
        for lang, dist in self._lang_dist.items():
            new_dist = (dist * self._population + request["lang_dist"][lang]
                        * request["population"])
            new_dist /= new_population
            self._lang_dist[lang] = new_dist

        self._population = new_population

    def process_immigration_queue(self):
        """
            Processes each immigration requests recieved in the current step.
        """
        while self._immigration_queue:
            request = self._immigration_queue.pop()
            self._process_immigration_request(request)
