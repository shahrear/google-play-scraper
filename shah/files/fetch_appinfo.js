var gplay = require('google-play-scraper');

var fs = require("fs");
var sqlite3 = require("sqlite3");

var log_file = './debug_fetchjs_mar25.log';
fs.truncateSync(log_file);
//
// only continue if the database exists
//
var repository = "androzoo_03242017";
fs.exists(repository, function(exists) {
if (exists) {

//
// open the database
//
var db = new sqlite3.Database(repository);
var loop_count = 0;

//"SELECT pkg_name FROM applist where markets like '%play.google.com%' and (app_type='' or app_type is null)"
var stmt ="SELECT sha256,pkg_name FROM applist where markets like '%play.google.com%' and pkg_name='kr.ac.snjc.library'";
//var stmt = "SELECT pkg_name FROM applist where markets like '%play.google.com%' and id between " + process.argv[2] + " and " +process.argv[3];
db.each(stmt, function(err, row) {
console.log('package name: '+row.pkg_name);
gplay.app({appId: row.pkg_name}).then( function ( lists ) {

      var app_details = JSON.stringify(lists);


      gplay.permissions({appId: row.pkg_name}).then( function (lists_perm) {

            var log_str = '';

            log_str += "---------------------------------------------------------\n";
            log_str += "Currently fetching app number: " + loop_count + '\n';
            log_str += "app sha256: " + row.sha256 + "\n";
            log_str += "app_id: " + lists.appId + "\n";
            log_str += "---------------------------------------------------------\n\n";

            var app_permissions = JSON.stringify(lists_perm);

            db.run("UPDATE applist SET app_details=?, app_permissions=?, app_genre=?, app_type=? WHERE sha256=?", [app_details,app_permissions,lists.genre,lists.genreId,row.sha256], function(err,uprow){

                  if(err)
                  {
                        fs.appendFileSync(log_file, "\nUpdate failed: sha256: " + row.sha256 + "\n");
                        console.log("\nUpdate failed: sha256: " + row.sha256 + "\n");
                  }
                  else {
                        log_str += "\nUpdate succeeded -- sha256: " + row.sha256 + "\n";
                        fs.appendFileSync(log_file, log_str);
                        console.log (log_str);

                  }

            });

      });

});

loop_count += 1;
});
db.close();
} else {
console.log("Database does not exist, run broker_node_init.js first.");
}
});
