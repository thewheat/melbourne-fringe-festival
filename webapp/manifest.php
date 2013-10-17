<?php
header("Content-Type: text/cache-manifest");
?>
CACHE MANIFEST

CACHE:
index.htm
css/foundation.min.css
css/normalize.css
css/style.css
js/foundation.min.js
js/handlebars.js
js/vendor/custom.modernizr.js
js/vendor/zepto.js
js/app.js
test/data_list.js
NETWORK:
*
<?php   echo "# Hash: " 
. md5_file('index.htm') 
. md5_file('js/app.js') 
. md5_file('test/data_list.js') 
. "\n"; ?>
