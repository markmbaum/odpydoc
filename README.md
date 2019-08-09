# odpydoc

This repo contains a Python module for creating HTML documentation of small to medium sized Python packages/modules. The `doc` function is the only public member of `odpydoc`. It accepts the name of a package or module as a string, imports the package, and generates HTML file(s) documenting the public objects in the package. Subpackages in the target package's `__all__` variable are recursively documented and linked to from their parent. The HTML files are styled after [Atom's](https://atom.io/) One Dark theme. `odpydoc` is not meant for large and complex packages like numpy. It collects all the target's docstrings and presents them in an easily navigable format with the option to view member's source code.

### usage
Simply pass the name of a module or package to `odpydoc.doc()` as a string, and it will drop HTML files in the desired directory.

### examples
* The automatically generated documentation for this module, `odpydoc`, is [here](http://markmbaum.github.io/odpydoc). There is only one public object in the module, so the docs are slim.

* As another example, [this](http://markmbaum.github.io/odpydoc/pdoc.html) is odpydoc's documentation for a Python package quite similar to `odpydoc`, called [`pdoc`](https://github.com/BurntSushi/pdoc). The `pdoc` package is more complete and flexible than `odpydoc`, but there are some differences. `odpydoc` generates HTML with a different style and will recursively document subpackages found in the `__all__` variable of a target package, automatically linking to the subpackage documentation from the parent's documentation.

* A simple example of the recursive documentation can be found [here](http://markmbaum.github.io/emf/), in the documentation for another one of my projects. The submodule names in the contents link to the documentation for those submodules.

##### dependencies
`os`, `inspect`, `importlib`, `textwrap`, `pygments`
