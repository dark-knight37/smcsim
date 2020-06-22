# smcsim
Smart Mixing Cell Simulator

## Objective
This repository is related to a simulator of a kind of flexible manufacturing system (FMS) named Smart Mixing Cell (SMC). The repository is under construction and, up to now, it has the aim to show how to use the simulator. The full description of the simulator context and overview is under evaluation in scientific journals.

## Repository structure
The repository is structured as follows:
* core: package of source code needed to run the simulation. This package refers to another Github repository (https://github.com/stefanomarrone/dse);
* robot: main folder containing the code developed over the core package;
* replication: results of the replication package.

## Replication package
The content of the *replication* folder is a serie of .ini files and .log files describing the inputs and the outputs of a series of experiments described in the sumbitted paper. To execute the batch, more to the main folder of the repository and run 


```
python3 batch_robot.py ./replication/
```

## How to build your experiment
If you want to prepare your own SMC configuration and run some experiments, you need to write a configuration file. There is no formal grammar for the configuration files, yet. Take the config.ini file as a starting example. To run in 

```
python3 test_robot.py inifilename logfile
```

In the logfile you'll find not only the final metrics but all the meaningful events of the simulation.

## License
The software is licensed according to the GNU General Public License v3.0 (see License file).

## Feedback
Anyone can report bugs on GitHub! Here's how it works:
* Click “New issue” and choose the appropriate format.
* Fill out the template with all the relevant info.

Feature requests are also welcome. Before opening a feature request, please take a moment to find out whether your idea fits with the scope and goals of the project. Please provide as much detail and context as possible.

**Thanks a ton for helping me making better software.**

## Credits
This software is build upon the following software library. Without it, building this software would be harder:
* Simpy ver 3.0.13
* configparser 
* numpy ver 1.18.4
* scipy ver 1.4.1