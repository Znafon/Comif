angular.module('comif.commande',
[
  'ui.router',
  'comifServices'
])

.config(function ($stateProvider) {

  $stateProvider
  .state('app.commande', {
    url: "/commande/:clientId",
    templateUrl: "app/commande/commande.html",
    controller: 'CommandeCtrl',
    resolve: {
      client: function(Client, $stateParams) {
        return Client.get({clientId: $stateParams.clientId}).$promise;
      },
      inventaire: function(Inventaire) {
        return Inventaire.query().$promise;
      }
    }
  });

})

.controller('CommandeCtrl', function(client, inventaire, baseUrl, Message, $scope, $http, $state) {

  $scope.client = client;
  $scope.inventaire = inventaire;
  $scope.commande = {};
  $scope.loading = false;

  var scope = $scope;

  $scope.addToCommand = function(item, categorieIndex, itemIndex) {
    if(scope.commande[item.id] === undefined) {
      scope.commande[item.id] = {
        id: item.id,
        nom: item.nom,
        prix: parseFloat(item.prix, 10),
        quantite: 1
      };
    } else {
      scope.commande[item.id].quantite += 1;
    }

    scope.inventaire[categorieIndex].items[itemIndex].nombre -= 1;
  };

  $scope.computeSolde = function() {
    var sum = 0;
    for(item in $scope.commande) {
      sum += parseFloat($scope.commande[item].prix, 10)*$scope.commande[item].quantite;
    }

    return $scope.client.solde - sum;
  };

  $scope.total = function() {
    var sum = 0;
    for(item in $scope.commande) {
      sum += parseFloat($scope.commande[item].prix, 10)*$scope.commande[item].quantite;
    }

    return sum;
  };

  $scope.minus = function(item) {
    $scope.commande[item.id].quantite -= 1;

    if ($scope.commande[item.id].quantite == 0) {
      delete $scope.commande[item.id];
    }

    for(var i = 0; i < $scope.inventaire.length; i++) {
      for(var j = 0; j < $scope.inventaire[i].items.length; j++) {
        if($scope.inventaire[i].items[j].id == item.id) {
          $scope.inventaire[i].items[j].nombre += 1;
        }
      }
    }

  };

  $scope.plus = function (item) {
    $scope.commande[item.id].quantite += 1;

    for(var i = 0; i < $scope.inventaire.length; i++) {
      for(var j = 0; j < $scope.inventaire[i].items.length; j++) {
        if($scope.inventaire[i].items[j].id == item.id) {
          $scope.inventaire[i].items[j].nombre -= 1;
        }
      }
    }
  };

  $scope.go = function () {
    $scope.loading = true;
    var p = {};

    for(id in $scope.commande) {
      p[id] = $scope.commande[id].quantite;
    }

    $http.get(baseUrl + '/commande/' + $scope.client.id,
    {
      params: p
    }).then(function successCallback(response) {
      $scope.loading = false;
      if(response.data.solde <= 0) {
        Message.warn("Le solde de "+ response.data.nom +" est de "+ response.data.solde +"€");
      } else {
        Message.info("Le solde de "+ response.data.nom +" est de "+ response.data.solde +"€");
      }
      $state.go('app.index');
    }, function errorCallback(response) {
      Message.danger("La commande n'a pas pu être effectuée.");
      $scope.loading = false;
    });
  };

})
