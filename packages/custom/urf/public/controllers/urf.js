'use strict';

/* jshint -W098 */
angular.module('mean.urf').controller('UrfController', ['$scope', 'Global', 'Urf',
  function($scope, Global, Urf) {
    $scope.global = Global;
    $scope.package = {
      name: 'urf'
    };
  }
]);
