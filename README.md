# odpydoc

This repo contains a small Python package for creating HTML documentation of other Python packages/modules. The `doc` function accepts the name of a package or module as a string, imports the package, and creates a single HTML file documenting the public objects in the package by inspecting the objects in the package. Subpackages in the target package's `__all__` variable are recursively documented and linked to from their parent module/package. The HTML files are styled after [Atom's](https://atom.io/) One Dark theme. So far, this code has not been able to handle large and complex packages like numpy. It's meant for relatively small packages and modules.

### usage
Simply pass the name of a module or package to `odpydoc.doc()` as a string, and it will drop HTML files in the current directory.

### examples
* The automatically generated documentation for this module, `odpydoc`, is [here](http://mbaum1122.github.io/odpydoc). There is only one public object in the module though, so the docs are boring.

* As another example, [this](http://mbaum1122.github.io/odpydoc/pdoc.html) is odpydoc's documentation for a Python package quite similar to `odpydoc`, called [`pdoc`](https://github.com/BurntSushi/pdoc). The `pdoc` package is more complete and flexible than `odpydoc`, but there are some differences. `odpydoc` generates HTML with a different style and will recursively document subpackages found in the `__all__` variable of a target package, automatically linking to the subpackage documentation from the parent's documentation.

* A simple example of the recursive documentation can be found [here](http://mbaum1122.github.io/emf/), in the documentation for another one of my projects. The submodule names in the contents link to the documentation for those submodules.

##### dependencies
* `inspect`
* `textwrap`
* `pygments`
