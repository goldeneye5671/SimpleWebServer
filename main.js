function getData(){
    ajaxGetRequest('/data/bar_graph.json', load_bar_graph);
    ajaxGetRequest('/data/line_graph.json', load_line_graph);
    ajaxGetRequest('/data/scatter_plot.json', load_scatter_plot);
}

function ajaxGetRequest(path, callback) {
    let request = new XMLHttpRequest();
    request.onreadystatechange = function() {
          if (this.readyState===4 && this.status ===200) {
              callback(this.response);
            }
    }
    request.open("GET", path);
    request.send();
}


function load_bar_graph(request){
    let bardata = JSON.parse(request);
    let data = []
    let dict = {'x': [], 'y': [], 'type':''};
    let layout = {'title': 'Building permits by month, Buffalo NY', 'xaxis':{'title':'month'}, 'yaxis': {'title':'# permits'}};
    for (let key of Object.keys(bardata)){
        if (key==1){
            dict['x'].push('January');
        }else if (key==2){
            dict['x'].push('February');
        }else if (key==3){
            dict['x'].push('March');
        }else if(key==4){
            dict['x'].push('April');
        }else if (key==5){
            dict['x'].push('May');
        }else if (key==6){
            dict['x'].push('June');
        }else if (key==7){
            dict['x'].push('July');
        }else if (key==8){
            dict['x'].push('August');
        }else if (key==9){
            dict['x'].push('September');
        }else if (key==10){
            dict['x'].push('October');
        }else if (key==11){
            dict['x'].push('November');
        }else if (key==12){
            dict['x'].push('December');
        }
    }
    for (let val of Object.values(bardata)){
        dict['y'].push(val);
    }
    dict['type'] = 'bar';
    data.push(dict);
    Plotly.plot('bar_graph', data, layout);
}


function load_line_graph(request){
    let linedata = JSON.parse(request);
        let data = [];
        let dict = {'x': [], 'y': [], 'type':''};
        let layout = {'title': 'Building permits by year, Buffalo NY', 'xaxis':{'title':'year'}, 'yaxis': {'title':'# permits'}};
        for (let key of Object.keys(linedata)){
            dict['x'].push(key);    
        }
        for (let val of Object.values(linedata)){
            dict['y'].push(val);
        }
        dict['type'] = 'scatter';
        data.push(dict);
        Plotly.plot('line_graph', data, layout);
}


function load_scatter_plot(request){
    let scatterdata = JSON.parse(request);
    let data = [];
    let trace = {'x':[], 'y':[], 'mode':'markers', 'type':'scatter', 'name':'', 'marker': {'size':12}};
    let counter = 0;
    let year = 2008;
    let layout = {'title': 'Total Value of Work, by project size and year', 'xaxis':{'title':'Total Value of Work ($)'}, 'yaxis': {'title':'Project Size'}};
    for (let values of Object.values(scatterdata)){
        for (let key of Object.keys(values)){
            if (key == 'low'){
                trace['y'].push('Small');
            }else if (key == 'med'){
                trace['y'].push('Medium')
            }else if (key == 'high'){
                trace['y'].push('Large')
            }
            trace['x'].push(values[key]);
        }
        trace['name'] = String(year);
        year++;
        data.push(trace);
        trace = {'x':[], 'y':[], 'mode':'markers', 'type':'scatter', 'name':'', 'marker': {'size':12}};
    }
    Plotly.plot('scatter_plot', data, layout);
}