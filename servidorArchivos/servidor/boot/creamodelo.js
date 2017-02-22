module.exports = function(app) {

  app.dataSources.cuentas.automigrate(['User'], function(err) { 
    if (err) throw err;
  });
}
