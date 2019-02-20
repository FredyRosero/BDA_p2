var data;
var nodes2 = []
var edges2 = []
var agents = []
var conex = []
var polarity = []
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       var myArr = JSON.parse(xhttp.responseText);
       toNodes(myArr);        
        var data = {
            nodes: nodes2,
            edges: edges2
        };
        var network = new vis.Network(container, data, options);        
    }
};
xhttp.open("GET", "php/relationships.php", true);
xhttp.send();

function toNodes(data) {
    console.log(data);
    ds = []
    i=0;
    conex = [] 
    for (var k in data){
        row = {id: k}
        //console.log( k, data[k] );
        conex[i]=[]   
        data[k].forEach(function(el) {                  
            for (var key in el){                
                if (key=='agent:a' || key=='agent:b' ) agents.push(el[key]);
                if (key=='agent:a') conex[i][0]=el[key];
                if (key=='agent:b') conex[i][1]=el[key];
                if (key=='agent:weight') conex[i][2]=el[key];
                if (key=='polarity:value') conex[i][3]=el[key];
            } 
        });
        i++;
    };
    agents = unique(agents);
    dictionary = {}
    i=1;
    agents.forEach(function(el) {
        dictionary[el]=i
        nodes2.push({id: i, label: el, font: {align: 'middle'}})
        i++;
    })
    agents = dictionary;        
    console.log(agents);
    conex.forEach(function(el) {
        edges2.push({   from: agents[el[0]], 
                        to:agents[el[1]], 
                        value:el[2],
                        label:el[3],                        
                        color: colorizer(el[3])
        });
    })
    console.log(edges2);
}

function colorizer(value) {
    return 'rgb('+map_range(value,-1.0,1.0,0,255)+",0,"+map_range(value,-1.0,1.0,255,0)+")";
}

function map_range(value, low1, high1, low2, high2) {
    return Math.round(low2 + (high2 - low2) * (value - low1) / (high1 - low1));
}

function unique(arr) {
    var u = {}, a = [];
    for(var i = 0, l = arr.length; i < l; ++i){
        if(!u.hasOwnProperty(arr[i])) {
            a.push(arr[i]);
            u[arr[i]] = 1;
        }
    }
    return a;
}
