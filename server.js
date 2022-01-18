const express = require('express');
const path = require('path');
const app = express();
const http = require('http')
const router = express.Router()
const url=require('url');

const fs = require('fs');


let {PythonShell} = require('python-shell')

app.use(
  express.urlencoded({
    extended: true
  })
)


app.post("/SSA", function(req, res) {
  var pyshell = new PythonShell('analysis/yes.py');
  pyshell.send(JSON.stringify(req.body.data))

  if (req.body.groups != null) {
    pyshell.send(req.body.groups)
  } else {
    pyshell.send('10')
  }

  if (req.body.window != null) {
    pyshell.send(req.body.window)
  } else {
    pyshell.send('10')
  }


  var totalMessage = ""
  pyshell.on('message', function (message) {
    totalMessage += (message)
  });

  // end the input stream and allow the process to exit
  pyshell.end(function (err) {
    res.send(totalMessage)
    res.end()
  })
});

app.post('/loadData', function(req, res) {  
  var start = (req.body.start);
  var end = (req.body.end);
  var ticker = (req.body.ticker)
    
  var pyshell = new PythonShell('analysis/import_data.py');
  pyshell.send(start)
  pyshell.send(end)

  if(ticker != null){
    pyshell.send(ticker)
  } else {
    pyshell.send('^GSPC')
  }

  var lastMessage = ""
  pyshell.on('message', function (message) {
    lastMessage = (message)
  });

  // end the input stream and allow the process to exit
  pyshell.end(function (err) {
    res.send(lastMessage);
    res.end()
  });
});






// must have an array of json objects with each entry having a 'y' key 
app.post('/SAAData', function(req, res) {  
  console.log('A')
  var pyshell = new PythonShell('analysis/singular_spectrum_with_inputs.py');
  pyshell.send(req.body.data)
  console.log('B')

  if (req.body.groups != null) {
    pyshell.send(req.body.groups)
  } else {
    pyshell.send('10')
  }

  if (req.body.window != null) {
    pyshell.send(req.body.window)
  } else {
    pyshell.send('10')
  }

  console.log('C')

  var totalMessage = ""
  pyshell.on('message', function (message) {
    totalMessage += (message)
  });

  // end the input stream and allow the process to exit
  pyshell.end(function (err) {
    console.log(totalMessage)
    res.send(totalMessage)
    res.end()
  });
});



const server = http.createServer(app);
const port = 3000
const io = require("socket.io")(server)
server.listen(port);





app.use(express.json());
app.use(express.static("express"));
// default URL for website
app.use('/', function(req,res){
    res.sendFile(path.join(__dirname+'/express/index.html'));
    //__dirname : It will resolve to your project folder.
  });


console.debug('Server listening on port ' + port);
console.log('Began Running at ' + (new Date()).toString())

io.on('connection', (socket) => {
  console.log("A user has joined")

  socket.on('stock market data request', ({start, end})=> {
    var pyshell = new PythonShell('analysis/import_data.py');
    pyshell.send('1990-01-01')
    pyshell.send('2021-07-12')

    var lastMessage = ""
    pyshell.on('message', function (message) {
      lastMessage = (message)
    });

    // end the input stream and allow the process to exit
    pyshell.end(function (err) {
        if (err) {
            throw err;
        };
        socket.emit('stock market data sent', lastMessage)
        // console.log(lastMessage)
        console.log('finished');
    });
  })
});


console.log("Done initializing server")