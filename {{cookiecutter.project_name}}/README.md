# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

_Created by: {{ cookiecutter.author_name }} (<{{ cookiecutter.author_email }}>)_<br>

<br>_Created for: {{ cookiecutter.project_name }}_ <br><br>

_Created on: MM/DD/YYYY_

## Project notes

### Staff involved

Reporter: TK name/email
Editor: TK name/email

### Documentation links

_TK: List relevant documents + planning sources_

### Published links

_TK: List of relevant published stories, graphics, etc._

### Data sources

_TK: List access info & contact info for data sources used in the project_

## Technical

An outline of the basic project structure is available in the [cookiecutter-datakit template repo](https://github.com/WashPost/cookiecutter-datakit).

### Set up project for the first time

1. Clone this {{ cookiecutter.project_name }} repo locally and enter `{{ cookiecutter.project_name }}/`.

2. Initialize your local project for S3 data integration:

   ```
   datakit data init
   ```

3. Sync your local project's data with the project data stored on s3. (For more on how data syncing works, see the [datakit-data plugin docs](https://datakit-data.readthedocs.io/en/latest/usage.html#data-push-pull)):

   ```
   datakit data pull
   ```

**If you will be using python for this project create a virtual environment** to easily manage required packages:

4. Create python virtual environment:

   ```
   source python_project_bootstrap.sh
   ```

- **_Note:_** Once you've created a virtual environment for your project, make sure to activate it each time before getting to work:
  - From `{{ cookiecutter.project_name }}/`:

    ```
    workon {{ cookiecutter.project_name }}
    ```

5. Install the project dependencies:

   ```bash
   uv sync
   ```

6. Run the pipeline:

   ```bash
   snakemake --cores all
   ```
