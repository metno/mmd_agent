Tests can be run by:

```bash
python -m pytest -vv --cov=mmd_agent --cov-report=term --cov-report=xml

```

# MMD Agent

[![flake8](https://github.com/metno/mmd_agent/actions/workflows/syntax.yml/badge.svg?branch=main)](https://github.com/metno/mmd_agent/actions/workflows/syntax.yml)
[![pytest](https://github.com/metno/mmd_agent/actions/workflows/pytest.yml/badge.svg?branch=main)](https://github.com/metno/mmd_agent/actions/workflows/pytest.yml)
[![codecov](https://codecov.io/gh/metno/mmd_agent/branch/main/graph/badge.svg?token=xSG9Sg0jQ0)](https://codecov.io/gh/metno/mmd_agent)

## Installation
```
git clone https://github.com/metno/mmd_agent

cd mmd_agent

mkdir unsent_mmd

```
Create the file `config.yaml` based on `example-config.yaml` and fill it with the following:

```
dmci_url:
unsent_mmd_path: unsent_mmd

``````
## Dependencies

For the main packages:

| Package      | PyPi                   | Ubuntu/Debian      | Source                                |
| ------------ | ---------------------- | ------------------ | ------------------------------------- |
| requests     | `pip install requests` | `python3-requests` | https://github.com/psf/requests       |
| pyyaml       | `pip install pyyaml`   | `python3-yaml`     | https://github.com/yaml/pyyaml        |
| 

The requirements can also be installed with:
```bash
pip install -r requirements.txt
```

## Environment Variables

The package reads the following environment variables.

* `MMS_PRODUCT_EVENT_MMD` mmd file in xml format.

## Tests

The tests use `pytest`. To run all tests for all modules, run:
```bash
python -m pytest -vv
```

To add coverage, and to optionally generate a coverage report in HTML, run:
```bash
python -m pytest -vv --cov=mmd_agent --cov-report=term --cov-report=html
```
Coverage requires the `pytest-cov` package.

## Usage

It consist of two scripts.
 - For posting MMD files to dmci api
 - For reposting the MMD files that were not sent while the dmci was down.

```python
MMS_PRODUCT_EVENT_MMD=$(cat <path to mmd file>) python agent.py
```

Then the mmd file is sent to the dmci api.

```python
python handler.py
```
This tries to repost the unsent MMD files that were persisted in 'unsent_mmd' while dmci was down.

## Licence

Copyright 2021 MET Norway

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in
compliance with the License. You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License
is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the License for the specific language governing permissions and limitations under the
License.

See Also: [LICENSE](https://raw.githubusercontent.com/metno/mmd_agent/main/LICENSE)
