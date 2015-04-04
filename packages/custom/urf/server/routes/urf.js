'use strict';

/* jshint -W098 */
// The Package is past automatically as first parameter
module.exports = function(Urf, app, auth, database) {

  app.get('/urf/example/anyone', function(req, res, next) {
    res.send('Anyone can access this');
  });

  app.get('/urf/example/auth', auth.requiresLogin, function(req, res, next) {
    res.send('Only authenticated users can access this');
  });

  app.get('/urf/example/admin', auth.requiresAdmin, function(req, res, next) {
    res.send('Only users with Admin role can access this');
  });

  app.get('/urf/example/render', function(req, res, next) {
    Urf.render('index', {
      package: 'urf'
    }, function(err, html) {
      //Rendering a view from the Package server/views
      res.send(html);
    });
  });
};
