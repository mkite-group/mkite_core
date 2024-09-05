<div align="center">
  <img src="https://raw.githubusercontent.com/mkite-group/mkite_core/main/docs/_static/mkite-core.png" width="300"><br>
</div>

# mkite-core: essentials for mkite

mkite_core offers a set of tools for the mkite suite. For example, it provides essential classes for recipes, plugins, and midware for models. mkite_core also offers some I/O support for interfacing mkite with other packages, such as rdkit.

## Documentation

General tutorial for `mkite` and its plugins are available in the [main documentation](https://mkite.org).
Complete API documentation is pending.

## Installation

`mkite_core` is essential to run all other components of mkite. To install this package, use pip:

```bash
pip install mkite_core
```

Alternatively, for a development version, clone this repo and install it in editable form:

```bash
pip install -U git+https://github.com/mkite-group/mkite_core
```

## Contributions

Contributions to the entire mkite suite are welcomed.
You can send a pull request or open an issue for this plugin or either of the packages in mkite.
When doing so, please adhere to the [Code of Conduct](CODE_OF_CONDUCT.md) in the mkite suite.

The mkite package was created by Daniel Schwalbe-Koda <dskoda@ucla.edu>.

### Citing mkite

If you use mkite in a publication, please cite the following paper:

```bibtex
@article{mkite2023,
    title = {mkite: A distributed computing platform for high-throughput materials simulations},
    author = {Schwalbe-Koda, Daniel},
    year = {2023},
    journal = {arXiv:2301.08841},
    doi = {10.48550/arXiv.2301.08841},
    url = {https://doi.org/10.48550/arXiv.2301.08841},
    arxiv={2301.08841},
}
```

## License

The mkite suite is distributed under the following license: Apache 2.0 WITH LLVM exception.

All new contributions must be made under this license.

SPDX: Apache-2.0, LLVM-exception

LLNL-CODE-848161
