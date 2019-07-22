# Language Distribution Predictor

The Language Distribution Predictor (LDP) is a proof of concept predictive model for forecasting the distribution of various spoken languages across the world in the near future.
Originally developed during the 2018 MCM competition, this release is a reimagining of the original project completed for problem B. Additional information concerning the original prompt can be found [here](https://www.comap.com/undergraduate/contests/mcm/contests/2018/problems/).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

LDP is a Python 3 command line script. If Python 3 is not already installed on your machine follow these [instructions](https://wiki.python.org/moin/BeginnersGuide/Download).

In order to run LDP the following prerequisite packages are required:
- [click](https://click.palletsprojects.com/en/7.x/)
- [pandas](https://pandas.pydata.org/)
- [plotly](https://plot.ly/python/)

The easiest way to install these is by using pip, which comes preinstalled with Python 3>=3.4 downloaded from python.org.

First, you'll need ensure that you have the latest version of pip.
```
pip install --upgrade pip
```
If you are using Windows it is recommended that you use the following instead:
```
python -m pip install --upgrade pip
```
Then you can run the following commands to install the required packages.
```
pip install click
pip install pandas
pip install plotly
```

### Installing

Download the project from GitHub and extract the folder to the directory of your choice.
Open the terminal and navigate to the directory you placed the project in.

To use the simulator, run

```
python ldp .\data\regiondata2017.json 50
```
This runs the simulation on the region structure described in the regiondata.json for 50 simulation cycles.

It should display the following in the console.
```
Running ldp simulation from .\data\regiondata2017.json for 50 cycles.
Pre Simulation Data:
  regions  english  spanish  french  chinese
0     USA    0.702    0.123   0.003    0.010
1     CAN    0.900    0.008   0.321    0.091
2     MEX    0.086    0.983   0.000    0.000
3     OTH    0.162    0.076   0.042    0.159

Post Simulation Results:
  regions   english   spanish    french   chinese
0     USA  0.652304  0.131556  0.018558  0.025431
1     CAN  0.699736  0.103941  0.070331  0.036628
2     MEX  0.154225  0.876193  0.003160  0.004134
3     OTH  0.163328  0.076126  0.041954  0.158649
```

## Usage

```
python ldp <file> <cycles> --display-language <lang> --output <location>
```

\<file>
: (required) location of the region data json file.

\<cycles>
: (required) number of simulation cycles to run.

-d \<lang> or --display-langauge \<lang>
: (optional) name of language to display distribution data for in choropleth chart.

-o \<location> or --output \<location>
: (optional) directory to save output files in.

### Example
```
python ldp ./data/regiondata2017.json 50 english
```
Report to console:
```
Running ldp simulation from .\data\regiondata2017.json for 50 cycles.
Pre Simulation Data:
  regions  english  spanish  french  chinese
0     USA    0.702    0.123   0.003    0.010
1     CAN    0.900    0.008   0.321    0.091
2     MEX    0.086    0.983   0.000    0.000
3     OTH    0.162    0.076   0.042    0.159

Post Simulation Results:
  regions   english   spanish    french   chinese
0     USA  0.652304  0.131556  0.018558  0.025431
1     CAN  0.699736  0.103941  0.070331  0.036628
2     MEX  0.154225  0.876193  0.003160  0.004134
3     OTH  0.163328  0.076126  0.041954  0.158649
```
Image in web browser:

![](/assets/englishplot.png)

## Versioning

We use [SemVer](http://semver.org/) for versioning.

## Authors

* **Jacob Lindey** - *Software Development*
* **William Davis** - *Statistical Analysis, Original Project*
* **Chris Ligato** - *Statistical Analysis, Original Project*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [This](https://www.karlsims.com/rd.html) Reaction-Diffusion explanation that acted as inspiration for the migration mechanics.
