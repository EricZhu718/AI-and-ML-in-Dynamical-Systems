const express = require('express');
const path = require('path');
const app = express();
const server = require('http').createServer(app);


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
  socket.emit("Welcome", "Hello")
  console.log("A user has joined")
});

console.log("Done initializing server")