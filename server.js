const express = require('express');
const path = require('path');
const app = express();
const http = require('http')
const router = express.Router()
const url=require('url');

const fs = require('fs');

app.use(
  express.urlencoded({
    extended: true
  })
)

app.post('/sub', function(request, response) {
  const htmlfile = 'express/testing.html'
  var html = fs.readFileSync(htmlfile).toString();
  response.send(html);
})

app.post("/add", function(req, res) {
  console.log(req.body)
  
  var num1 = Number(req.body.num1);
  var num2 = Number(req.body.num2);
    
  var result = num1 + num2 ;
    
  res.send("Addition - " + result);
});

app.post('/loadData', function(req, res) {
  
  console.log(req.body)
  
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
    });
});


const server = http.createServer(app);



const port = 3000
const io = require("socket.io")(server)
server.listen(port);

let {PythonShell} = require('python-shell')




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
        if (err){
            throw err;
        };
        socket.emit('stock market data sent', lastMessage)
        // console.log(lastMessage)
        console.log('finished');
    });
  })
});


console.log("Done initializing server")