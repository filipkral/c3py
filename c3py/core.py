"""Interactive c3js carts with Python"""

import os
import json

def _read_file_as_string(filepath):
    txt = ""
    with open(filepath) as fl:
        txt = fl.read()
    return txt

def _parse_data(data, asjson=True):
    """Convert data into the right form.
    The way c3 plots are generated expects data as  [{k1 -> v11, k2 -> v21}, {k1 -> v12, k2 -> v22}, ...]
    This function makes sure the input data is coverted to that form.
    It tries to make some guesses to allow other data formats such as:
        Dictionary like {k1: [v11, v21, ...], k2: [v12, v22], ...}
        Pandas data frame.
        Path to a file with json input.
    """
    newdata = None
    if type(data) is str:
        if os.path.isfile(data):
            # assume file with json in the right form
            with open(data) as fl:
                newdata = json.dumps(json.loads(fl.read()))
        else:
            # assume json in the right form
            newdata = data
    elif hasattr(data, "to_json"):
        # assume pandas data frame
        newdata = data.to_json(orient="records")
    elif type(data) is dict:
        # assume dict of lists
        newdata = []
        keys = list(data.keys())
        for i in range(min([len(data[k]) for k in keys])):
            record = dict([[k,data[k][i]] for k in keys])
            newdata.append(record)
    elif type(data) is list or type(data) is tuple:
        # assume list or tuple of dicts in the right form
        newdata = data
    else:
        raise Exception("Unexpected c3py data format or shape.")

    if asjson and type(data) is not str:
        newdata = json.dumps(data)

    return newdata


def scatterplot(data, xkey, ykey, out, title=None, xlab='', ylab='', singlefile=True, localport=None):
    """Make c3 scatterplot of xkey and ykey variables in data.
    data -- dict or json like [{k1 -> v11, k2 -> v21}, {k1 -> v12, k2 -> v22}, ...]
    xkey -- name of the key of each record in data to use on x axis
    ykey -- name of the key of each record in data to use on y axis
    out -- path to the output file
    title -- output page title
    singlefile -- Embed everithing into a single html file? Default is True.
    localport -- port number where there is a server runing on localhost.
        Default is None, which does nothing.
        If specified, Python will open the web browser at localhost:<loaclport>/<name of output file>
    """

    thisdir = os.path.dirname(os.path.abspath(__file__))
    _osj = os.path.join


    # Should resources like style sheets, js files, and data be baked into a single file?
    singlefile = True

    if singlefile:
        c3css = '<style type="text/css">{0}</style>'.format(_read_file_as_string(_osj(thisdir, 'c3.min.css')))
        jqueryjs = '<script type="text/javascript">\n{0}\n</script>'.format(_read_file_as_string(_osj(thisdir, 'jquery.min.js')))
        d3js =  '<script type="text/javascript">\n{0}</script>'.format(_read_file_as_string(_osj(thisdir, 'd3.min.js')))
        c3js =  '<script type="text/javascript">\n{0}\n</script>'.format(_read_file_as_string(_osj(thisdir, 'c3.min.js')))
    else:
        c3css = '<link href="https://cdnjs.cloudflare.com/ajax/libs/c3/0.4.10/c3.min.css" media="screen" rel="stylesheet" type="text/css" />'
        jqueryjs = '<script src="//code.jquery.com/jquery-1.12.0.min.js"></script>'
        d3js = '<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.15/d3.min.js"></script>'
        c3js = '<script src="https://cdnjs.cloudflare.com/ajax/libs/c3/0.4.10/c3.min.js"></script>'

    if title is None:
         title = "Scatter plot of {0} and {1}".format(xkey, ykey)

    markup = _read_file_as_string(_osj(thisdir, 'template-c3py.html'))\
            .replace('{{xlab}}', xlab)\
            .replace('{{ylab}}', ylab)\
            .replace('{{xkey}}', xkey).replace('{{xkey}}', xkey)\
            .replace('{{ykey}}', ykey).replace('{{ykey}}', ykey)\
            .replace('{{c3css}}', c3css)\
            .replace('{{jqueryjs}}', jqueryjs)\
            .replace('{{d3js}}', d3js)\
            .replace('{{c3js}}', c3js)\
            .replace('{{title}}', str(title)).replace('{{title}}', str(title))\
            .replace('{{data}}', _parse_data(data))


    with open(out, "w") as outf:
        outf.write(markup)

    if localport is not None:
        import webbrowser
        webbrowser.open('http://localhost:{0}/{1}'.format(localport, os.path.basename(out)))

    return out

if __name__ == "__main__":
    data = [
        {"station": 123, "discharge": 3.4, "level": 1.2},
        {"station": 124, "discharge": 1.4, "level": 0.2},
        {"station": 125, "discharge": 3.2, "level": 1.8}
    ]
    outfile= r'C:\temp\c3py\out.html'
    scatterplot(data, 'discharge', 'level', outfile)

    data = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sampledata', 'data_records.json')
    outfile= r'C:\temp\c3py\out2.html'
    scatterplot(data, 'discharge', 'level', outfile)

