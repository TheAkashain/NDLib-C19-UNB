# Scripts to be Submitted with Slurm

We run scripts in the cluster
[Cedar](https://docs.computecanada.ca/wiki/Cedar)
of [Compute Canada](https://docs.computecanada.ca/wiki/Compute_Canada_Documentation).

```
ssh cedar.computecanada.ca
```

Upload the following files into a single folder.

```
setup_python3.sh
submit.sh
gathering_simulation.py
myGroupNetwork.py
network_data.json
```

Run the following commands.

```
sh setup_python3.sh
sbatch submit.sh
```

This should generate the outputs
```gathering_simulation.csv```
and ```sizes_vs_nums.jpg```
in the same folder.

## Inside the Scripts

- The script ```setup_python3.sh```
is to load *Python 3*
because the default setting on the server
is *Python 2*.

The script ```submit.sh``` is as follows.
Note that the option **--time** can be customized.

```
#!/bin/bash
#SBATCH --time=00:10:00
python ./gathering_simulation.py > gathering_log.txt
```

Details of Slurm can be found through
[this link](https://slurm.schedmd.com/quickstart.html).