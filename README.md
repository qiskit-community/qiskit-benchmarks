# Qiskit Transpiler Contribution Benchmarks

Researchers and Qiskit transpiler contributors need an easy way to compare different passes and passmanagers. The website https://qiskit-community.github.io/qiskit-benchmarks provides a visual way to make that comparison. This repository handles the benchmarking test suite, as well as the list of passmanagers to compare. 

## How can I add my contribution

Fork this repository and create a PR with an entry in [`contributions.yaml`](https://github.com/qiskit-community/qiskit-benchmarks/blob/master/contributions.yaml). The format is:

```yaml
- <pip requirement specifier>:
  - <module>:<passmanager constructor>
  - <module>:<passmanager constructor>
```

The `<pip requirement specifier>` is a reference to your 