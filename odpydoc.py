"""This is a module for creating HTML documentation of other Python packages/modules. The doc_module function accepts the name of a package or module as a string, imports the package, and creates a single HTML file documenting the public objects in the package by inspecting the objects in the package. Subpackages in the target package's __all__ variable are recursively documented. The HTML files are styled after Atom's One Dark theme."""

import inspect
import textwrap
from os import path
from pygments import highlight as _highlight
from pygments.lexers import PythonLexer as _PythonLexer
from pygments.formatters import HtmlFormatter as _HtmlFormatter

_fn_base = path.dirname(__file__)
with open(path.join(_fn_base, 'odpydoc.js'), 'r') as _ifile:
    _js = _ifile.read()
with open(path.join(_fn_base, 'odpydoc.css'), 'r') as _ifile:
    _css = _ifile.read()
with open(path.join(_fn_base, 'one-dark-pygments.css'), 'r') as _ifile:
    _css += _ifile.read()
del(_ifile)

_python_lexer = _PythonLexer()
_html_formatter = _HtmlFormatter()

def _is_number(s):
    """Check if an element can be converted to a float, returning `True`
    if it can and `False` if it can't"""
    if((s is False) or (s is True)):
        return(False)
    else:
        try:
            float(s)
        except(ValueError, TypeError):
            return(False)
        else:
            return(True)

def _get_public_vars(obj):
    """Call the builtin vars function on an object to retrieve its __dict__ and remove all keys starting with an underscore
    args:
        obj - the object to retrieve public variables from"""
    v = vars(obj)
    v = dict(zip([k for k in v if (k[0] != '_')],
                [v[k] for k in v if (k[0] != '_')]))
    return(v)

def _nav_html(mod_name, submodules, functions, classes, others):
    """Generate an unordered list of links for the navigation menu/index of the documentation
    args:
        mod_name - str, the name of the module being documented
        submodules - dict, a dictionary of submodules in the module being
                     documented
        functions - dict, a dictionary of function objects in the module
                    being documented
        classes - dict, a dictionary of class objects in the module
                  being documented
        others - dict, a dictionary of other objects in the module
                 being documented, like globally used floats or strings
    returns:
        html - an HTML string representing the navigation bar"""
    #wrap in a single dict for iteration
    keys = ['submodules', 'functions', 'classes', 'others']
    d = dict(zip(keys, [submodules, functions, classes, others]))
    html = """<div id="nav-wrapper">
                <div id="nav">
                    <h2>contents</h2>
                    <ul id="nav-ul">"""
    for k in keys:
        if(d[k]):
            html += """
            <li class="nav-li"><a href="#%s">%s</a>
                <ul class="subnav-ul">""" % (k, k)
            for m in sorted(d[k].keys()):
                if(k == 'submodules'):
                    href = '%s.html' % m
                else:
                    href = '#%s' % m
                if(k == 'classes'):
                    html += '<li class="subnav-li"><a href="%s">%s</a>' % (href, m)
                    #get properties and methods
                    properties, methods = dict(), dict()
                    v = vars(d[k][m])
                    for var_name in v:
                        if(var_name[0] != '_'):
                            if(inspect.isdatadescriptor(v[var_name])):
                                properties[var_name] = v[var_name]
                            if(inspect.ismethod(v[var_name]) or (inspect.isfunction(v[var_name]))):
                                methods[var_name] = v[var_name]
                    #create sublists
                    if(properties or methods):
                        html += '<ul class="subsubnav-ul">'
                        if(properties):
                            html += '<li class="subsubnav-li"><a href=#%s-properties>properties</a>' % m
                            html += '<ul class="subsubsubnav-ul">'
                            for p in sorted(properties.keys()):
                                html += '<li class="subsubsubnav-li">'
                                html += '<a href=#%s-%s>%s</a></li>' % (m, p, p)
                            html += '</ul></li>'

                        if(methods):
                            html += '<li class="subsubnav-li"><a href=#%s-methods>methods</a>' % m
                            html += '<ul class="subsubsubnav-ul">'
                            for n in sorted(methods.keys()):
                                html += '<li class="subsubsubnav-li">'
                                html += '<a href=#%s-%s>%s</a></li>' % (m, n, n)
                            html += '</ul></li>'

                        html += '</ul>'

                    html += '</li>'
                else:
                    html += '<li class="subnav-li"><a href="%s">%s</a></li>' % (href, m)
            html += '</ul>'
    html += '</ul></div></div>'
    return(html)

def _get_docstr(obj):
    """Pull the docstring of an object and format it for HTML
    args:
        obj - target object
    returns:
        docstr - an HTML string or an empty string"""
    tab = '&ensp;'*4
    docstr = obj.__doc__
    if(docstr):
        docstr = docstr.strip()
        docstr = docstr.replace('\n', '<br>'
                ).replace('\t', tab).replace('    ', tab)
        return('<p class="docstr">%s</p>' % docstr)
    else:
        return('')

def _get_source(obj):
    """Pull the source string of an object and format it for HTML
    args:
        obj - target object
    returns:
        sourcestr - an HTML string"""
    #get source as a list of lines
    try:
        lines = inspect.getsourcelines(obj)[0]
    except(IOError):
        return(None)
    else:
        #break any long running lines (those softwrapped by an editor)
        for i in range(len(lines)):
            if(len(lines[i]) > 100):
                l = lines[i]
                indent = l.replace(l.lstrip(), '')
                lines[i] = textwrap.fill(lines[i], width=81,
                        subsequent_indent=indent)
                lines[i] += '\n'
        #return the source in a <pre>
        source = ''.join(lines).replace('\t', '    ')
        source = _highlight(source, _python_lexer, _html_formatter)
        source = """
                <div class="source">
                    <h4 onclick="toggleSource(this)">show source</h4>
                    <div class="code">
                        %s
                    </div>
                </div>""" % source
        return(source)

_function_arg = lambda s: '<span class="function-arg">' + str(s) + '</span>'
_default_str = lambda s: """<span class="default-str">'""" + str(s) + "'</span>"

def _get_argstr(function):
    """Get the argument string for a function, with appropriate highlighting
    args:
        function - a function object
    returns:
        html - an HTML string"""
    #get the argspec named tuple
    argspec = list(inspect.getargspec(function))
    #remove 'self'
    if('self' in argspec[0]):
        argspec[0].pop(argspec[0].index('self'))
    #apply spans for syntax coloring
    for i in range(len(argspec[0])):
        argspec[0][i] = _function_arg(argspec[0][i])
    if(argspec[1]):
        argspec[1] = _function_arg(argspec[1])
    if(argspec[2]):
        argspec[2] = _function_arg(argspec[2])
    if(argspec[3]):
        argspec[3] = list(argspec[3])
        for i in range(len(argspec[3])):
            arg = argspec[3][i]
            if("'" in repr(arg)):
                argspec[3][i] = _default_str(arg)
            elif(_is_number(arg)):
                argspec[3][i] = _function_arg(arg)
            elif((arg is True) or (arg is False) or (arg is None)):
                argspec[3][i] = _function_arg(arg)

    #join default arg names with their values
    if(argspec[3] is not None):
        for i in range(1, len(argspec[3]) + 1):
            argspec[0][-i] += '=%s' % str(argspec[3][-i])
    #concatenate the complete string
    argstr = '('
    if(argspec[0]):
        argstr += ', '.join(argspec[0])
    if(argspec[1]):
        if(argspec[0]):
            argstr += ', '
        argstr += '*' + argspec[1]
    if(argspec[2]):
        if(argspec[1] or argspec[0]):
            argstr += ', '
        argstr += '**' + argspec[2]
    argstr += ')'
    return(argstr)

def _function_to_html(F, name):
    """Create an HTML string for a function object
    args:
        F - target function object
        name - str, the name of the function
    returns:
        html - an HTML string for the function"""
    try:
        #open a div
        html = '<div class="function" id="%s">' % name
        #add the function name and argstr
        html += '<p class="function-str"><span class="function-name">%s</span>%s</p>' % (name, _get_argstr(F))
        #add the docstr
        html += _get_docstr(F)
        #get the source
        source = _get_source(F)
        if(source):
            html += source
        #close the div
        html += '</div>'
        return(html)
    except(TypeError):
        return('')

def _functions_to_html(functions):
    """Create an HTML string for a dictionary of functions, alphabetically
    args:
        functions - dict containing the functions, indexed by their names
    return:
        html - an HTML string"""
    #start the html
    html = ''
    if(functions):
        html += '<div class="section" id="functions"><h2>functions</h2>'
        for k in sorted(functions.keys()):
            html += _function_to_html(functions[k], k)
        html += '</div>'
    return(html)

def _property_to_html(P, name, classname):
    """Get an HTML string for a property object
    args:
        P - target property object
        name - str, the name of the property
        classname - str, the name of the class where the property is defined
    returns:
        html - an HTML string"""
    html = '<div class="property" id="%s-%s">' % (classname, name)
    html += '<p class="property-name">%s</p>' % name
    html += _get_docstr(P) + '</div>'
    return(html)

def _class_to_html(C, name):
    """Create an html string for a class/type object
    args:
        C - class object
        name - str, the class object's name
    returns:
        html - an HTML string"""
    #get it's variables, properties, and methods
    v = _get_public_vars(C)
    #open a div for this individual class
    html = '<div class="class" id="%s">' % name
    #add the class name
    html += '<h3>%s</h3>' % name
    #add the class docstr
    if(C.__doc__):
        html += _get_docstr(C)
    #add the class-constructor
    if('__init__' in vars(C)):
        init = vars(C)['__init__']
        html += _function_to_html(init, name).replace('id="%s"' % name, '')
    #allocate separate strings for properties, methods
    properties, methods = '', ''
    for k in sorted(v.keys()):
        #check if property
        if(inspect.isdatadescriptor(v[k])):
            if(properties == ''):
                properties += '<div class="properties" id="%s-properties"><h4>Properties</h4>' % name
            properties += _property_to_html(v[k], k, name)
        #check if method
        if(inspect.ismethod(v[k]) or (inspect.isfunction(v[k]))):
            if(methods == ''):
                methods += '<div class="methods" id="%s-methods"><h4>Methods</h4>' % name
            methods += _function_to_html(v[k], k).replace(
                    'id="%s"' % k, 'id=%s-%s' % (name, k))
    if(properties != ''):
        properties += '</div>'
    if(methods != ''):
        methods += '</div>'
    html += properties + methods
    #close the individual class's div
    html += '</div>'
    return(html)

def _classes_to_html(classes):
    """Convert a dictionary of class/type objects into html documentation strings
    args:
        classes - dict mapping class/type names to class/type objects
    returns:
        html - an HTML string"""
    #start html string
    html = ''
    #proceed alphabetically
    if(classes):
        #section div for all classes
        html = '<div class="section" id="classes"><h2>classes</h2>'
        for k in sorted(classes.keys()):
            html += _class_to_html(classes[k], k)
        html += '</div>'
    return(html)

def _others_to_html(others):
    """Create an html string for a dictionary of objects like floats or strings
    args:
        others - dict mapping object names to objects
    returns:
        html - an HTML string"""

    tab = '&ensp;'*4

    if(others):
        html = '<div class="section" id="others"><h2>others</h2>'
        for k in sorted(others.keys()):
            comments = inspect.getcomments(others[k])
            if(not comments):
                comments = ''
            else:
                comments.replace('\n', '<br>')
                comments = """<div class="comments">%s</div>""" % comments
            t = str(type(others[k])).split("'")[1]
            t = t.replace('<', '&#60;').replace('>', '&#62;')
            html += """
                <div class="other" id="%s">
                    <span class="other-name">%s</span><br>
                    %s<span class="other-type">type:</span>%s<br>
                    %s<span class="other-value">value:</span><pre>%s</pre>
                    %s
                </div>""" % (
                    k,
                    k,
                    tab, t,
                    tab, textwrap.fill(repr(others[k]), width=81),
                    comments)
        html += '</div>'
        return(html)
    else:
        return('')

def doc(mod, **kw):
    """This is the main function of odpydoc. It documents a module/package by importing it and inspecting the objects it contains, creating HTML strings for them and spitting out a single HTML file. Subpackages in the target package's __all__ variable are recursively documented.
    args:
        mod - str, module name or module object"""

    #import the module if a string is passed in
    if(type(mod) is str):
        try:
            exec('import %s as mod' % mod)
        except(ImportError, SyntaxError) as e:
            print(e)
            print('Cannot import "%s"' % mod)
            return(None)
    #store the module name
    mod_name = mod.__name__

    #get the module's dictionary/namespace/whatever
    try:
        v = vars(mod)
    except(TypeError):
        return(None)
    #check for submods in __all__
    if('__all__' in v):
        submods_in_all = v['__all__']
        for submod_name in submods_in_all:
            doc(v[submod_name])
    else:
        submods_in_all = []
    #remove private keys
    v = _get_public_vars(mod)
    #separate the objects in v based on their types
    submodules, functions, classes, others = dict(), dict(), dict(), dict()
    for k in v:
        t = type(v[k])
        if(inspect.ismodule(v[k])):
            if(k in submods_in_all):
                submodules[k] = v[k]
        elif(inspect.isfunction(v[k])):
            functions[k] = v[k]
        elif(inspect.isclass(v[k])):
            classes[k] = v[k]
        else:
            others[k] = v[k]

    #GENERATE HTML
    #get the module docstring, if any
    mod_docstring = _get_docstr(mod)
    if(mod_docstring):
        mod_docstring = ('<div class="section">%s</div>' %
                mod_docstring.replace('class="docstr"', 'id="mod-docstr"'))

    html = ("""
    <html lang="en">
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <title>%s</title>
            <link href="https://fonts.googleapis.com/css?family=Anonymous+Pro|Open+Sans" rel="stylesheet">
            <style>%s</style>
    	</head>
        <body onresize="arrange()" onload="arrange()">

            <!--Back to Top Button-->
            <a id="back-to-top" href="#">back to top</a>

            <!--Navigation Sidebar-->
            %s

            <div id="main">
                <h1>%s</h1>
                <!--module docstring section-->
                %s

                <!--functions section-->
                %s

                <!--classes section-->
                %s

                <!--others section-->
                %s
            </div>

        </body>

        <!--Control the width and height of the #main element-->
        <script type="text/javascript">%s</script>

    </html>
    """ %
    (mod_name,
    _css,
    _nav_html(mod_name, submodules, functions, classes, others),
    mod_name,
    mod_docstring,
    _functions_to_html(functions),
    _classes_to_html(classes),
    _others_to_html(others),
    _js))

    #delete the module
    del(mod)

    fn = mod_name + '.html'
    with open(fn, 'w') as ofile:
        ofile.write(html)
    print('documentation written to: %s' % fn)
