var app = angular.module('recVerify',['ngRoute']);

app.config(function($routeProvider){
  $routeProvider
    .when('/record',{
      templateUrl: 'partials/record.html'
    })
    .when('/phonetics',{
      templateUrl: 'partials/phonetics.html'
    })
    .when('/good',{
      templateUrl: 'partials/good.html'
    })
});
