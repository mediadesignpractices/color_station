var exif = require('exiftool');
var fs   = require('fs');

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
        console.log('writing...');
        fs.writeFile('./output/meta1.csv', metadata, function (err) {   //still doesn't write
          if (err) throw err;
          console.log('It\'s saved!');
          console.log(metadata);
        });
      }
    });
  }
});