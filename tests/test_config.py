"""
MMD_AGENT : MMD Agent Test
==================

Copyright 2021 MET Norway

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import pytest
import os
import logging
from mmd_agent.config import read_config


LOGGER = logging.getLogger(__name__)


@pytest.mark.mmd_agent
def test_read_config(filesDir, rootDir):
    """Test reading config file."""

    # Read some values and see that we get them
    confFile = os.path.join(filesDir, "config.yaml")
    exampleConf = os.path.join(rootDir, "example_config.yaml")

    # Fake path
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        read_config(configFile="not_a_real_file")
    assert pytest_wrapped_e.type == SystemExit

    # value for dmci_url doesn't exist

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        read_config(configFile=exampleConf)
    assert pytest_wrapped_e.type == SystemExit

    # Cause the open command to fail
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        read_config(configFile=confFile)
    assert pytest_wrapped_e.type == SystemExit