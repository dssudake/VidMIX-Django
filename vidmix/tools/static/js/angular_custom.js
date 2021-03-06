var app = angular.module("angularApp", [])

app.config(function ($interpolateProvider) {
  $interpolateProvider.startSymbol('{$');
  $interpolateProvider.endSymbol('$}');
});

app.config(['$httpProvider', function ($httpProvider) {
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);
app.controller("btnCtrl", function ($scope, $rootScope) {
  $scope.mtitle = "";
  $scope.single = function (music, title, start) {
    $rootScope.mtitle = title;
    if (document.getElementById("player1").getAttribute("src") === music) {
      var myAudio = document.getElementById("player1");
      return myAudio.paused ? myAudio.play() : myAudio.pause();
    }
    else {
      document.getElementById("player1").pause();
      document.getElementById("player1").setAttribute('src', music);
      document.getElementById("player1").load();
      document.getElementById("player1").play();
      document.getElementById("vplay").currentTime = start;
      document.getElementById("title").innerHTML = title;
    }
  };
  $scope.double = function () {
    $('#audioUpload').modal('toggle');
  };
});


//----------------- Audio Replace Handle ------------------
app.directive('fileModel', ['$parse', function ($parse) {
  return {
    restrict: 'A',
    link: function (scope, element, attrs) {
      var model = $parse(attrs.fileModel);
      var modelSetter = model.assign;

      element.bind('change', function () {
        scope.$apply(function () {
          modelSetter(scope, element[0].files[0]);
        })
      })
    }
  }
}])

app.service('multipartForm', ['$http', function ($http) {
  this.post = function (uploadUrl, data) {
    var fd = new FormData();
    for (var key in data)
      fd.append(key, data[key]);

    $http.post(uploadUrl, fd, {
      transformRequest: angular.indentity,
      headers: { 'Content-Type': undefined }
    }).then(function success(response) {
      console.log(response.data.success);
      document.getElementById("download").className = "visible";
      document.getElementById("replaceVplay").load();
      var display = response.data.success;
      display.concat("Audio For subtitle",response.data.audioid,"has been changed, Go to COMPARE to see changes")
      $('#audioUpload').modal('hide');
      alert(response.data.success.concat(" Audio For subtitle ", response.data.audioid," has been changed, Go to compare to see changes"));
    }, function error(response) {
      alert(response.statusText);
    });
  }
}])

app.controller('formCtrl', ['$scope', 'multipartForm', function ($scope, multipartForm) {
  $scope.replace = {};
  $scope.submit = function ($event) {
    $event.preventDefault();
    var videoId = window.location.pathname.split('/')[3];
    var uploadUrl = "/upload/".concat(videoId, "/", $scope.mtitle, "/");
    multipartForm.post(uploadUrl, $scope.replace);
  }
}]);