var gplay = require('google-play-scraper');

var fs = require("fs");
var mysql = require("mysql");
var stream = require('stream');
var moment = require('moment');
var HashTable = require('hashtable');
var hashtable = new HashTable();


var log_file = './debug_fetchjs_'+process.argv[4]+'.log';
//fs.truncateSync(log_file);
var log_str = '';
log_str += "---------------------------------------------------------\n";
var now = moment()
var formatted = now.format('YYYY-MM-DD HH:mm:ss Z')

log_str += "New run, time: " + formatted + '\n\n';
log_str += "arg1: " + process.argv[2] + " arg2: " + process.argv[3] + " arg3: " + process.argv[4]+'\n';
console.log(log_str);
fs.appendFileSync(log_file, log_str);
//
// only continue if the database exists
//
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'shahrear',
  password : '$Obscure123',
  database : 'androzoo'
});

 hashtable.put(-1, 'dummy');


connection.connect(function(err){
if(!err) {
    console.log("Database is connected ... nn\n");

    //"SELECT pkg_name FROM applist where markets like '%play.google.com%' and (app_type='' or app_type is null)"
    //var stmt = "SELECT id,sha256,pkg_name FROM applist where id between 1 and 10";
    var stmt = "SELECT id,pkg_name,sha256 FROM applist where markets like '%play.google.com%' and (app_type='' or app_type is null) and id between " + process.argv[2] + " and " + process.argv[3];
    connection.query(stmt)
    .stream()
    .pipe(stream.Transform({
          objectMode:true,
          transform: function(row,encoding,callback) {
                console.log('package name: '+row.pkg_name);
                hashtable.put(row.id, row.pkg_name);

                gplay.app({appId: row.pkg_name}).then( function ( lists ) {

                var app_details = JSON.stringify(lists);


                      gplay.permissions({appId: row.pkg_name}).then( function (lists_perm) {

                            var app_permissions = JSON.stringify(lists_perm);
                            //console.log(app_details+'\n\n');
                           // console.log(app_permissions);
                            connection.query("UPDATE applist SET app_details=?, app_permissions=?, app_genre=?, app_type=? WHERE id=?", [app_details,app_permissions,lists.genre,lists.genreId,row.id], function(err,uprow){

                                  if(err)
                                  {
                                        log_str = '';

                                        log_str += "---------------------------------------------------------\n";
                                        log_str += "Currently fetching app db id: " + row.id + '\n';
                                        log_str += "package: " + row.pkg_name + "\n";
                                        log_str += "---------------------------------------------------------\n\n";
                                        log_str += "\nUpdate failed: db id: " + row.id + "\nerr: "+err+"\n";

                                        fs.appendFileSync(log_file, log_str);
                                        console.log("\nUpdate failed: id: " + row.id + " err: "+err+"\n");
                                  }
                                  else {
                                        log_str = '';

                                        log_str += "---------------------------------------------------------\n";
                                        log_str += "Currently fetching app db id: " + row.id + '\n';
                                        log_str += "package: " + row.pkg_name + "\n";
                                        log_str += "---------------------------------------------------------\n\n";
                                        log_str += "\nUpdate succeeded: id: " + row.id + "\n";
                                        fs.appendFileSync(log_file, log_str);
                                        console.log (log_str);

                                  }

                                  hashtable.remove(row.id);

                            });

                      });
                },function(error) {
                      connection.query("UPDATE applist SET app_details=?, app_permissions=?, app_genre=?, app_type=? WHERE id=?", ['not in market now','shahvoid','shahvoid','shahvoid',row.id], function(err,uprow){

                           if(err)
                           {
                                  log_str = '';

                                  log_str += "---------------------------------------------------------\n";
                                  log_str += "Currently fetching app db id: " + row.id + '\n';
                                  log_str += "package: " + row.pkg_name + "\n";
                                  log_str += "---------------------------------------------------------\n\n";
                                  log_str += '\npackage not found in store: '+row.pkg_name+'\n';
                                  log_str += "\nUpdate failed: db id: " + row.id + "\nerr: "+err+"\n";

                                  fs.appendFileSync(log_file, log_str);
                                    console.log('\npackage not found in store: '+row.pkg_name);
                                  console.log("\nUpdate failed: id: " + row.id + " err: "+err+"\n");
                           }
                           else {
                                 log_str = '';

                                 log_str += "---------------------------------------------------------\n";
                                 log_str += "Currently fetching app db id: " + row.id + '\n';
                                 log_str += "package: " + row.pkg_name + "\n";
                                 log_str += "---------------------------------------------------------\n\n";
                                 log_str += '\npackage not found in store: '+row.pkg_name+'\n';
                                   log_str += "\nUpdate succeeded: id: " + row.id + "\n";

                                  fs.appendFileSync(log_file, log_str);
                                   console.log('\npackage not found in store: '+row.pkg_name);

                           }



                      });

                        hashtable.remove(row.id);
                  });


                callback();
          }
    })
      .on('finish',function() { console.log('done');hashtable.remove(-1);}));


} else {
    console.log("Error connecting database ... nn");
}
});

(function wait () {
   if (hashtable.size()>0)
   {
         console.log('\nhashtable not empty, sleeping for 1000\n');
         setTimeout(wait, 1000);
   }
   else {
         console.log('hashtable size: '+hashtable.size()+'\n process exiting, processed: '+process.argv[2]+'  and '+process.argv[3]);
         connection.end();
         process.exit();
   }

})();
