var comifServices = angular.module('comifServices', ['ngResource', 'base64']);

comifServices.config(['$resourceProvider', function($resourceProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;
}])

.config(['$httpProvider',
  function(provider){
    provider.defaults.xsrfCookieName = 'csrftoken';
    provider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

comifServices.value('baseUrl', 'http://localhost/api'); // A remplacer par une config

comifServices.factory('Client', ['$resource', 'baseUrl',
  function($resource, baseUrl){
    return $resource(baseUrl + '/clients/:clientId',
    {
      clientId: ''
    },
    {
      query: {
        method: 'GET',
        isArray: true,
      },
      update: {
        method: 'PUT'
      }
    });
}]);

comifServices.factory('Inventaire', function($resource, baseUrl) {
  return $resource(baseUrl + '/inventaire/', {}, {
    query: {
      method: 'GET',
      isArray: true
    }
  });
});

comifServices.factory('Message', function ($rootScope) {

  send = function(level) {
    return function(message, log) {
      if (log === "" || log === undefined) {
        error = "";
      } else {
        error = " ("+ log +")"
      }
      $rootScope.$broadcast('message', {
        level: level,
        text: message + error
      })
    }
  }

  return {
    info: send('info'),
    danger: send('danger'),
    warn: send('warning'),
    success: send('success')
    }
  }
);

comifServices.factory('Modal', function($rootScope) {
  return {
    deleteClient: function(client) {
      $rootScope.$broadcast('modal-delete-client', client);
    },
    addArgent: function (client) {
      $rootScope.$broadcast('modal-add-argent', client);
    },
    addClient: function () {
      $rootScope.$broadcast('modal-add-client');
    }
  }
});

comifServices.factory('User', function($http, baseUrl, $base64, $rootScope) {
  var username;

  var login = function(u, p) {
    var auth = "Basic " + $base64.encode(u + ':' + p);

    $http({
      method: 'GET',
      url: baseUrl + '/login',
      headers: {
        'Authorization': auth
      }
    }).then(function (response) {
      $http.defaults.headers.common.Authorization = auth;
      username = u;
      $rootScope.$broadcast('login-success');
    }, function (response) {
      $rootScope.$broadcast('login-fail');
    })
  }

  var logout = function () {
    username = undefined;
    $http.defaults.headers.common.Authorization = '';
    $rootScope.$broadcast('logout');
  }

  return {
    username: function() {
      return username;
    },
    login: login,
    logout: logout
  }
});
