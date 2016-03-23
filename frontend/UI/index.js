angular.module('comif',
[
  'ui',
  'ui.router',
  'ui.bootstrap.contextMenu',
  'ngAnimate',
  'ngIdle',

  'comifServices',
  'comifHelpers',
  'comif.login',
  'comif.client-detail',
  'comif.clients-list',
  'comif.sidebar',
  'comif.user',
  'comif.commande'
])

.run(function($rootScope, $state, $location, User, Idle){
  $rootScope.$on('$stateChangeStart', function(event, toState, toParams, fromState, fromParams){
    var u = User.username();
    if  (toState.name !== 'login' && u === undefined){
      $location.url('/login');
    }
  });

  $rootScope.$on('IdleTimeout', function () {
    User.logout();
    document.location.href = document.location.origin + '/#/login';
  });

  Idle.watch();
})

.run(function($rootScope) {
    $rootScope.keys = Object.keys;
})

.config(function (IdleProvider, TitleProvider) {
  IdleProvider.idle(3*60); // logout apres 3 minutes
  IdleProvider.timeout(1);
  TitleProvider.enabled(false);
})

.config(function($animateProvider) {
  $animateProvider.classNameFilter(/^(?:(?!ng-animate-disabled).)*$/);
})

.config(function($stateProvider, $urlRouterProvider) {

  $urlRouterProvider.otherwise("/login");

  $stateProvider
  .state('app', {
    abstract: true,
    templateUrl: "app/app.html"
  });
});
