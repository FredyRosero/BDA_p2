<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">

  <title>The HTML5 Herald</title>
  <meta name="description" content="BDA">
  <meta name="author" content="Fredy">

  <link rel="stylesheet" href="css/styles.css?v=1.0">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
</head>

<body>
    <button id="refresh">refresh</button>
    <div id="container"></div>
    <div id="mynetwork"></div>  
    <script src="js/scripts.js"></script>
    <script type="text/javascript">
        var container = document.getElementById('mynetwork');
        var options = {
            nodes:  {    shape: 'dot'
                    
            },
            edges:  {   width:3,
                        scaling:{label:{ min:8, max:12 }},
                        font: {align: 'horizontal'}
            }
        };
    </script>


</body>
</html>
