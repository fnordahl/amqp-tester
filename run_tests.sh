#!/bin/sh
#
# Copyright 2017 Frode Nordahl
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
VENV=.venv
if [ -d ${VENV} ]; then
    echo "Cleaning up virtualenv..."
    rm -rf ${VENV}
fi
if [ ! -d ${VENV} ]; then
    echo "Installing virtualenv..."
    virtualenv -q ${VENV}
    echo "Installing test-requirements..."
    ${VENV}/bin/pip install -r test-requirements.txt
fi

OK=1
run() {
    $*
    RET=$?
    if [ ${RET} -ne 0 ]; then
        echo "FAILURE (${0} exited with status ${RET}.)" 1>&2
        OK=0
    fi
}

echo "Running tests..."

run ${VENV}/bin/pep8 --exclude=${VENV} --statistics .
run ${VENV}/bin/flake8 --exclude=${VENV} --statistics

if [ ${OK} -gt 0 ]; then
    echo "SUCCESS" 1>&2
fi
