#!/bin/sh

if [ "$#" -ne 3 ]; then
  echo "Invalid number of parameters."
  echo "Provide the folder where to run the benchmarks, the contribution index and the output file."
  echo "I.e.: sh generate.sh _benchmark contributions.yaml www/data.json"
  exit 1
fi

BENCHMARK_PATH=$1
CONTRIBUTIONS_INDEX=$(realpath $2)
OUTPUT_PATH=$(realpath $3)

pushd() {
  command pushd "$@" &> /dev/null
}

popd() {
  command popd "$@" &> /dev/null
}

create_virtual_env() {
  echo "Creating virtual environment..."
  mkdir -p "$BENCHMARK_PATH"

  echo "Setup benchmark environment"
  cp -r benchmarkenv/* "$BENCHMARK_PATH"

  pushd "$BENCHMARK_PATH"
  python3 -m venv .venv
  source .venv/bin/activate

  echo "Check version:"
  python3 --version
  echo "Install common dependencies"
  pip3 install -r requirements.txt &> /dev/null

  echo "Take snapshot of the base benchmark environment"
  git init
  git add . &> /dev/null
  git commit -m'Add base virtual environment' &> /dev/null

  echo

  deactivate
  popd
}


run_benchmark() {
  pushd "$BENCHMARK_PATH"
  source .venv/bin/activate

  contributions=$(python3 extract_contributions.py "${CONTRIBUTIONS_INDEX}")
  for one_contribution in $contributions
  do
    echo "Running benchmarks for ${one_contribution}..."
    echo "Restore base benchmark environment"
    git checkout . &> /dev/null
    git clean --force -d &> /dev/null
    echo "Install contribution"
    pip3 install "${one_contribution}" &> /dev/null
    echo "Run benchmarks"
    python3 test_entry_points.py "${CONTRIBUTIONS_INDEX}" "${one_contribution}" "${OUTPUT_PATH}"
    echo
  done

  deactivate
  popd

  echo "Done."
}

create_virtual_env
run_benchmark