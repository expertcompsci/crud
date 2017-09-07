angular.module('birdsApp', ['ngRoute', 'ngSanitize'])
  .config(function($routeProvider, $locationProvider) {
    $routeProvider.
    when("/", {
      templateUrl: '/ng_templates/select.html',
      controller: MainCntl
    }).
    when("/index", {
      templateUrl: '/ng_templates/select.html',
      controller: MainCntl
    }).
    when("/detail/:id", {
      templateUrl: '/ng_templates/detail.html',
      controller: DetailCntl
    }).
    when("/new", {
      templateUrl: '/ng_templates/new.html',
      controller: NewCntl
    }).
    otherwise({
      redirectTo: '/index'
    });
    $locationProvider.html5Mode(true);
  })
  .service('db', function($http) {
    return {
      	getBirds: function(pg) {
				  	return $http.get('/api/birds?pg=' + pg);
      	},
      	getBird: function(id) {
				  return $http.get('/api/bird?id=' + id);
      	},
      	getPageCount: function(id) {
				  return $http.get('/api/pagecount');
      	},
		addBird: function(bird) {
			return $http.post('/api/addbird', bird);
		},
		updateBird: function(bird) {
			return $http.post('/api/updatebird', bird);
		},
		deleteBird: function(id) {
			return $http.delete('/api/deletebird?id=' + id);
		},
		searchBirds: function(target) {
			return $http.get('/api/searchbirds?target=' + target);
		},
		getTarget: function() {
			return $http.get('/api/gettarget');
		}
    };
  })

MainCntl.$inject = ['$scope', 'db', '$route', '$location', '$window'];
function MainCntl($scope, db, $route, $location) {
	$scope.pg = 0;
	$scope.id = 0;
	$scope.target = db.getTarget().then(function(target){
		$scope.target = target.data.target;	
	});
	$scope.pageCount = db.getPageCount().then(function(count) {
		$scope.pageCount = count.data.pagecount;
	});
	
	db.getBirds($scope.pg).then(function(birds) {
		$scope.birds = birds.data;
	});
	
	$scope.prevPage = function() {
		if ($scope.pg > 0) {
			$scope.pg--;
		}
	}
	
	$scope.prevPageDisabled = function() {
		return $scope.pg === 0 ? "disabled" : "";
	}

	$scope.nextPage = function() {
		if ($scope.pg < $scope.pageCount) {
			$scope.pg++;
		}
	}
	
	$scope.nextPageDisabled = function() {
		return $scope.pg >= $scope.pageCount ? "disabled" : "";
	}
	
	$scope.newBird = function() {
		$location.url('/new');
	}

	$scope.haveBirdData = function() {
		return (((typeof $scope.bird) != 'undefined') && ((typeof $scope.bird.id) != 'undefined'));
	}
	$scope.haveBirds = function() {
		if($scope.target != "") {
			return true;
		}
		if (((typeof $scope.birds) != 'undefined')) {
			if (($scope.birds.length > 0)) {
				return true;
			}
		}
		return false;
	}

	$scope.gotoPage = function (pg) {
		$scope.pg = pg;
	}

	$scope.$watch("pg", function(newValue, oldValue) {
		db.getBirds($scope.pg).then(function(birds) {
			$scope.birds = birds.data;
		});
	});

	$scope.$watch("target", function(newValue, oldValue) {
		if(((typeof newValue) != 'undefined') && (newValue != oldValue)) {
			db.searchBirds(newValue).then(function(birds) {
				$scope.birds = birds.data
				$scope.pg = 0;
				$scope.pageCount = db.getPageCount().then(function(count) {
					$scope.pageCount = count.data.pagecount;
				});
			})
		}
	})

}

DetailCntl.$inject = ['$scope', 'db', '$route', '$location', '$window'];
function DetailCntl($scope, db, $route, $location, $window) {
	$scope.edit = false;
	db.getBird($route.current.params.id).then(function(bird) {
		$scope.bird = bird.data;
	});

	$scope.updateBird = function() {
		console.log($scope.bird)
		console.log($scope.bird.id)
		db.updateBird($scope.bird)
		$location.url('/index');
	}

	$scope.deleteBird = function(id) {
		db.deleteBird(id);
		$window.location.href = '/index';
	}
}

NewCntl.$inject = ['$scope', 'db', '$route', '$location', '$window'];
function NewCntl($scope, db, $route, $location, $window) {
	$scope.bird = { "english_name": "", "sci_name": "", "flight_range": "", "bio_order": "", "family": "", "category": "" }
	$scope.init=true;
	$scope.addBird = function() {
		db.addBird($scope.bird).then(function(data) {
			$location.url = '/index';
		})
	}

	$scope.cancel = function() {
			$location.url = '/index';
	}
}

