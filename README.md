# zindi_load_default
## Environment
This repository makes use of `Git` version control. `Precommit` hooks have been used to provide checks to the developer on the heath and conformity of their code. Here, we make use of `Black` for automatic formatting, `flake8` for linting and `jupytext` to automatically convert our notebooks to `py:percent` files for better version control. Our environment has been setup using `Anaconda`. You can find an explicit environment file in the `src` directory. We have provideded a `Dockerfile` and compose to aid in portabilit of our environment. This project makes use of `kedro` for data versioning, project templating, data pipelining, automatic documentation, data catalogingm packaging and context management. Please refer to `conf/base/catalog` for speific details on how our data and models were extracted, serialized and versioning. The majority of our analysis has relied on consumer hardware with 16GB of Micron MT53E1G32D4NQ-046 memory clocked at 4267MHz and a Quadcore Intel R Core TM i7-1065G7 processor clocked at 1.30GHz, running Ubuntu 20.04 using linux kernel 5.4.0-48-generic. At the release of our work, we are unaware of any known issues in the software and hardware used by our analysis which may affect the reliability of our results.

## Model Serving
We have relied on MLFLOW (https://www.mlflow.org/docs/latest/models.html) and kedro-mlflow (https://github.com/Galileo-Galilei/kedro-mlflow) for model serving, which provide a simple specification for model serving on Azure, Sagemaker and Databricks. You can launch our baseline model as a REST API locally using `mlflow models serve -m mlruns/1/.` and navigate tracked artefacts using `kedru mlflow ui`.


## Overview

This is your new Kedro project, which was generated using `Kedro 0.16.5`.

Take a look at the [Kedro documentation](https://kedro.readthedocs.io) to get started.

## Rules and guidelines

In order to get the best out of the template:

* Don't remove any lines from the `.gitignore` file we provide
* Make sure your results can be reproduced by following a [data engineering convention](https://kedro.readthedocs.io/en/stable/11_faq/01_faq.html#what-is-data-engineering-convention)
* Don't commit data to your repository
* Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `conf/local/`

## How to install dependencies

Declare any dependencies in `src/requirements.txt` for `pip` installation and `src/environment.yml` for `conda` installation.

To install them, run:

```
kedro install
```

## How to run your Kedro pipeline

You can run your Kedro project with:

```
kedro run
```

## How to test your Kedro project

Have a look at the file `src/tests/test_run.py` for instructions on how to write your tests. You can run your tests as follows:

```
kedro test
```

To configure the coverage threshold, go to the `.coveragerc` file.

## Project dependencies

To generate or update the dependency requirements for your project:

```
kedro build-reqs
```

This will copy the contents of `src/requirements.txt` into a new file `src/requirements.in` which will be used as the source for `pip-compile`. You can see the output of the resolution by opening `src/requirements.txt`.

After this, if you'd like to update your project requirements, please update `src/requirements.in` and re-run `kedro build-reqs`.

[Further information about project dependencies](https://kedro.readthedocs.io/en/stable/04_kedro_project_setup/01_dependencies.html#project-specific-dependencies)

## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `context`, `catalog`, and `startup_error`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have run `kedro install` you will not need to take any extra steps before you use them.

### Jupyter
To use Jupyter notebooks in your Kedro project, you need to install Jupyter:

```
pip install jupyter
```

After installing Jupyter, you can start a local notebook server:

```
kedro jupyter notebook
```

### JupyterLab
To use JupyterLab, you need to install it:

```
pip install jupyterlab
```

You can also start JupyterLab:

```
kedro jupyter lab
```

### IPython
And if you want to run an IPython session:

```
kedro ipython
```

### How to convert notebook cells to nodes in a Kedro project
You can move notebook code over into a Kedro project structure using a mixture of [cell tagging](https://jupyter-notebook.readthedocs.io/en/stable/changelog.html#cell-tags) and Kedro CLI commands.

By adding the `node` tag to a cell and running the command below, the cell's source code will be copied over to a Python file within `src/<package_name>/nodes/`:

```
kedro jupyter convert <filepath_to_my_notebook>
```
> *Note:* The name of the Python file matches the name of the original notebook.

Alternatively, you may want to transform all your notebooks in one go. Run the following command to convert all notebook files found in the project root directory and under any of its sub-folders:

```
kedro jupyter convert --all
```

### How to ignore notebook output cells in `git`
To automatically strip out all output cell contents before committing to `git`, you can run `kedro activate-nbstripout`. This will add a hook in `.git/config` which will run `nbstripout` before anything is committed to `git`.

> *Note:* Your output cells will be retained locally.

## Package your Kedro project

[Further information about building project documentation and packaging your project](https://kedro.readthedocs.io/en/stable/03_tutorial/05_package_a_project.html)
