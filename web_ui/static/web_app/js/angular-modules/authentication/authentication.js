var authModule = angular.module('authModule',['ngRoute'])

authModule.service("AuthService", function(){
    function url_base64_decode(str){
        return window.atob(str)
    }

    this.url_base64_decode = url_base64_decode
})

authModule.controller('AuthCtrl', function($scope, $http, $window, AuthService){
    $scope.user = {username: '', password: ''}
    $scope.isAuthenticated = false

    $scope.submit = function (){
        $http
            .post('api/login', $scope.user)
            .then(function (response, status, headers, config){
                $window.sessionStorage.token = response.data.token;
                $scope.isAthenticated = true;
                $scope.message = "Success! Loading application";
                $window.location.href = '/index'
            })
            .catch(function(response, status, headers, config){
                delete $window.sessionStorage.token;
                $scope.isAuthenticated = false;
                $scope.message = response.data;
            })
    }

    $scope.logout = function() {
        $scope.isAuthenticated = false;
        alert("loggedOut!")
    }
});

authModule.factory("authInterceptor", function($rootScope, $q, $window){
    return {
        request: function(config){
            config.headers = config.headers  || {};
            if ($window.sessionStorage.token){
                config.headers.Authorization = 'Bearer ' + $window.sessionStorage.token;
            }
            return config;
        },
        responseError: function(rejection){
            if (rejection.status === 401){
                //Manage common 401 actions
            }
            return $q.reject(rejection);
        }
    };
});

authModule.config(function ($httpProvider){
    $httpProvider.interceptors.push('authInterceptor');
});

authModule.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}]);
