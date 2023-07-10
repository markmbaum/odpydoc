# odpydoc

This repo contains a Python module for quickly creating HTML documentation for Python packages/modules. It produces html files indexing members of the target module/package, organizing their docstrings, and including source code snippets. It recursively documents submodules in the target's `__all__` variable.

It has only one public function: `doc(mod, outdir=".", index=True, script=None)`.

* `mod` - the target module/package as a string
* `outdir` - output directory for the
* `index` - whether to name the top module index.html or name if after the package
* `script` - the path to a javascript file to include in the \<head\>

It's not meant for big complex packages. I made it to quickly document my own little packages as needed.

### intstalling

1. clone
2. run `pip install .` in the odpydoc directory

### using

either
* `import odpydoc` and use the `doc` function
* run `python -m odpydoc <module>` for your

### examples
* The automatically generated documentation for odpydoc itself is [here](http://markmbaum.github.io/odpydoc). There's only one public object in the module, so the docs are slim.

* For another example, [this](http://markmbaum.github.io/odpydoc/pdoc.html) is odpydoc's documentation for (an old version of) a Python package similar to odpydoc called [pdoc](https://github.com/BurntSushi/pdoc).

* A simple example of the recursive documentation can be found [here](http://markmbaum.github.io/emf/), the documentation for another one of my old projects. The submodule names in the contents link to the documentation for those submodules.
