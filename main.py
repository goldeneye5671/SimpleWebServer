import bottle
import json
import appcode


print('Successfully imported!!\n')

@bottle.route("/")
def index():
    return bottle.static_file('index.html', root='.')


@bottle.route("/main.js")
def main():
    return bottle.static_file("main.js", root='.')


@bottle.route("/data/bar_graph.json")
def dataBarGraph():
    appcode.loadData("permitData.csv", 5000)
    csv_data = appcode.readDataFromCSVFile('permitData.csv')
    temp_data = {}
    counter = 0
    count = {}
    
    for i in range (1, 13):
        counter = 0
        temp_data = appcode.filterByMonth(csv_data, i)
        for entry in temp_data:
            counter+=1
        count[i] = counter
    
    appcode.convertToJSON('bar_graph', count)
    
    return bottle.static_file('bar_graph.json', root='.')


@bottle.route("/data/line_graph.json")
def dataLineGraph():
    appcode.loadData("permitData.csv", 5000)
    csv_data = appcode.readDataFromCSVFile('permitData.csv')
    temp_data = {}
    counter = 0
    count = {}
    
    for i in range (2010, 2020):
        counter = 0
        temp_data = appcode.filterByYear(csv_data, i)
        for entry in temp_data:
            counter += 1
        count[i] = counter
    
    appcode.convertToJSON('line_graph', count)

    return bottle.static_file('line_graph.json', root='.')


@bottle.route("/data/scatter_plot.json")
def dataScatterPlot():
    appcode.loadData("permitData.csv", 5000)
    csv_data = appcode.readDataFromCSVFile('permitData.csv')
    temp_data1 = {}
    low = []
    med = []
    high = []
    count = {}
    
    for i in range(2008, 2020):
        temp_data1 = appcode.filterByYear(csv_data, i)
        low = appcode.filterInRange(temp_data1, 'value', 0, 5000)
        med = appcode.filterInRange(temp_data1, 'value', 5000, 50000)
        high = appcode.filterInRange(temp_data1, 'value', 50000, 500000)
        total_low = 0.0
        total_med = 0.0
        total_high = 0.0
        for dictionary in low:
            total_low += float(dictionary['value'])
        for dictionary in med:
            total_med += float(dictionary['value'])
        for dictionary in high:
            total_high += float(dictionary['value'])
        count[i] = {'low':total_low, 'med':total_med, 'high':total_high}

    appcode.convertToJSON('scatter_plot', count)
    return bottle.static_file('scatter_plot.json', root='.')


bottle.run(host='0.0.0.0', port=8080, debug=True)