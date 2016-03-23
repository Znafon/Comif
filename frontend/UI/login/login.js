angular.module('comif.login',
[
  'ui.router',
  'comifServices'
])

.config(function ($stateProvider) {

  $stateProvider
  .state('login', {
    url: '/login',
    templateUrl: 'login/login.html',
    controller: 'LoginCtrl'
  });

})

.controller('LoginCtrl', function($scope, User, $state) {
  $scope.loading = false;
  $scope.loginFailed = false;

  $scope.$on('login-fail',function () {
    $scope.loginFailed = true;
    $scope.loading = false;
  });

  $scope.$on('login-success', function() {
    $scope.loginFailed = false;
    $state.go('app.index');
  });

  $scope.go = function () {
    $scope.loading = true;
    User.login($scope.username, $scope.password);
  }
});
