(function () {
  'use strict';

  angular.module('app', [
    'ui.router'
  ])
  .config(['$stateProvider', '$urlRouterProvider', stateConfig]);

  function stateConfig($stateProvider, $urlRouterProvider) {
    $stateProvider
    .state('app', {
      url: '/home',
      templateUrl: 'app/home/home.html'
    });

    $urlRouterProvider.otherwise('/home');
  }
})();
