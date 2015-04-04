'use strict';

angular.module('mean.urf').config(['$stateProvider',
  function($stateProvider) {
    $stateProvider.state('urf example page', {
      url: '/urf/example',
      templateUrl: 'urf/views/index.html'
    });
  }
]);
