#c3py

This is a Pythonmodule that can produce HTML+CS+JS page to show data on an iteractive plot.
The output page uses [masayuki0812's c3 JavaScript library](https://github.com/masayuki0812/c3) which is based on mbostock's [d3](https://github.com/mbostock/d3).

# Requirements
+ Python 2.7
+ Webrowser such as Chrome

# Example
```
import c3py

data = [
    {"station": 123, "discharge": 3.4, "level": 1.2},
    {"station": 124, "discharge": 1.4, "level": 0.2},
    {"station": 125, "discharge": 3.2, "level": 1.8}
  ]
c3py.scatterplot(data=data, xkey='discharge', ykey='level', out='c:/temp/c3chart.html')
```
You may need to view the output page in a web browser as if the page was hosted on a server.
Python comes with a built-in webserver class that can resolve this. To see the chart from the example above:
```
# open command line and type
cd c:/temp
python.exe -m SimpleHTTPServer 8081
# then open your web browser and visit
http://localhost:8081/c3chart.html
```

