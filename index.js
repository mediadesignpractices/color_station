var exif = require('exiftool');
var fs   = require('fs');
var fs   = require('fast-csv');



fs.readFile('./test-data/IMG_1019.JPG', ['exiftool', '-csv', '-r'], 
  function (err, data) {
  if (err)
    throw err;
  else {
    exif.metadata(data, function (err, metadata) {
      if (err){
        throw err;
      }
      else{
        var stream = fs.createReadStream("meta.csv");
        console.log('writing...');
        fs.writeFile('./output/meta1.csv', metadata, function (err) {   //still doesn't write
          if (err) throw err;
          console.log('It\'s saved!');
          console.log(metadata);
          var csvStream = csv()
          .on("data", function(metadata){
               console.log(metadata);
          })
          .on("end", function(){
               console.log("done");
          });
        stream.pipe(csvStream);
        });
      }
    });
  }
});

//or
/*
var csvStream = csv
    .parse()
    .on("data", function(data){
         console.log(data);
    })
    .on("end", function(){
         console.log("done");
    });

stream.pipe(csvStream);

*/