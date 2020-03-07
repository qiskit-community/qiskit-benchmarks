#!/bin/sh

if [ "$#" -ne 3 ]; then
  echo "Invalid number of parameters."
  echo "Provide the folder where to run the benchmarks, the contribution index and the output file."
  echo "I.e.: bash generate.sh _benchmark contributions.yaml www/data.json"
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
  echo "🌍 Creating virtual environment..."
  mkdir -p "$BENCHMARK_PATH"

  echo "🛠  Setup benchmark environment"
  cp -r benchmarkenv/* "$BENCHMARK_PATH"

  pushd "$BENCHMARK_PATH"
  python3 -m venv .venv
  source .venv/bin/activate

  echo "🐍 Check version:"
  python3 --version
  echo "📦 Update pip"
  python3 -m pip install --upgrade pip &> /dev/null
  echo "📦 Install common dependencies"
  python3 -m pip install -r requirements.txt &> /dev/null

  echo "📸 Take snapshot of the base benchmark environment"
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
    echo "Restore base benchmark environment"
    git checkout . &> /dev/null
    git clean --force -d &> /dev/null
    echo "📦 Install contribution ${one_contribution}"
    python3 -m pip install "${one_contribution}"
    if [ $? == 0 ]; then
      echo "⏱  Run benchmarks"
      python3 test_entry_points.py "${CONTRIBUTIONS_INDEX}" "${one_contribution}" "${OUTPUT_PATH}"
    else
      echo "😱 Error installing contribution!"
    fi
    echo
  done

  deactivate
  popd

  echo "👌 Done."
}

create_virtual_env
run_benchmark