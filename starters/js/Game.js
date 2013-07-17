var fs = require('fs');

exports.game = {
	'bot' : null,
	'currentTurn' : -1,
	'myID' : -1,
	'orders' : [],
	'planets' : [],
	'fleets' : [],

	'numPlanets' : function() {
		return this.planets.length;
	},
	'getPlanet' : function(planetID) {
		return this.planets[planetID];
	},

	'numFleets' : function() {
		return this.fleets.length;
	},
	'getFleet' : function(fleetID) {
		return this.fleets[fleetID];
	},

	'myPlanets' : function() {
		var result = [];
		for ( var i = 0, len = this.planets.length; i < len; ++i) {
			var p = this.planets[i];
			if (p.owner == this.myID) {
				result.push(p);
			}
		}
		return result;
	},

	'myMilitaryPlanets' : function() {
		var result = [];
		for ( var i = 0, len = this.planets.length; i < len; ++i) {
			var p = this.planets[i];
			if (p.owner == this.myID && p.type == 'M') {
				result.push(p);
			}
		}
		return result;
	},

	'neutralPlanets' : function() {
		var result = [];
		for ( var i = 0, len = this.planets.length; i < len; ++i) {
			var p = this.planets[i];
			if (p.owner == 0) {
				result.push(p);
			}
		}
		return result;
	},

	'ennemyPlanets' : function() {
		var result = [];
		for ( var i = 0, len = this.planets.length; i < len; ++i) {
			var p = this.planets[i];
			if (p.owner != 0 && p.owner != this.myID) {
				result.push(p);
			}
		}
		return result;
	},

	'notMyPlanets' : function() {
		var result = [];
		for ( var i = 0, len = this.planets.length; i < len; ++i) {
			var p = this.planets[i];
			if (p.owner != this.myID) {
				result.push(p);
			}
		}
		return result;
	},

	'myFleets' : function() {
		var result = [];
		for ( var i = 0, len = this.fleets.length; i < len; ++i) {
			var fleet = this.fleets[i];
			if (fleet.owner == this.myID) {
				result.push(fleet);
			}
		}
		return result;
	},
	'enemyFleets' : function() {
		var result = [];
		for ( var i = 0, len = this.fleets.length; i < len; ++i) {
			var fleet = this.fleets[i];
			if (fleet.owner != this.myID) {
				result.push(fleet);
			}
		}
		return result;
	},

	'distance' : function(sourcePlanet, destinationPlanet) {
		var source = planets[sourcePlanet];
		var destination = planets[destinationPlanet];
		var dx = source.x - destination.x;
		var dy = source.y - destination.y;
		return Math.ceil(Math.sqrt(dx * dx + dy * dy));
	},

	'numShips' : function(playerID) {
		var numShips = 0;
		for ( var i = 0, len = this.planets.length; i < len; ++i) {
			var p = this.planets[i];
			if (p.owner == playerID) {
				numShips += p.numShips;
			}
		}
		for ( var i = 0, len = this.fleets.length; i < len; ++i) {
			var f = this.fleets[i];
			if (f.owner == playerID) {
				numShips += f.numShips;
			}
		}
		return numShips;
	},
	
	/**
	 *  Do NOT touch the following methods
	 */
	'start' : function(botInput) {
		this.bot = botInput;
		this.planets = [];
		this.fleets = [];

		var partialline = "";
		process.stdin.resume();
		process.stdin.setEncoding('utf8');
		var thisoutside = this;
		process.stdin.on('data', function(chunk) {
			var lines = chunk.split("\n");
			lines[0] = partialline + lines[0];
			partialline = "";
			// Complete lines will leave an empty
			// string at the end, if that is not the case
			// buffer this line until the next chunk
			if (lines[lines.length - 1] !== "") {
				partialline = lines[lines.length - 1];
				lines.splice(lines.length - 1, 1);
			}
			for ( var i = 0, len = lines.length; i < len; ++i) {
				thisoutside.processLine(lines[i]);
			}
		});
	},
	'processLine' : function(line) {
		line = line.trim().split(' ');
		
		if(line[0] === 'go') {
			this.myID = parseInt(line[1]);
			this.bot.onTurn();
			return;
		} else if(line[0] === 'end') {
			this.bot.onEnd();
			return;
		}
		
		if (line.length != 0) {
			if (line[0] == "M") {
				if (line.length != 5) {
					return 1;
				}
				this.planets.push({
					'type' : 'M',
					'id' : this.planets.length,
					'x' : parseInt(line[1]),
					'y' : parseInt(line[2]),
					'owner' : parseInt(line[3]),
					'numShips' : parseInt(line[4])
				});
			} else if (line[0] == "E") {
				if (line.length != 6) {
					return 1;
				}
				this.planets.push({
					'type' : 'E',
					'id' : this.planets.length,
					'x' : parseInt(line[1]),
					'y' : parseInt(line[2]),
					'owner' : parseInt(line[3]),
					'numShips' : parseInt(line[4]),
					'revenue' : parseInt(line[5])
				});
			} else if (line[0] == "F") {
				if (line.length != 7) {
					return 1;
				}
				this.fleets.push({
					'owner' : parseInt(line[1]),
					'numShips' : parseInt(line[2]),
					'sourcePlanet' : parseInt(line[3]),
					'destinationPlanet' : parseInt(line[4]),
					'totalTripLength' : parseInt(line[5]),
					'turnsRemaining' : parseInt(line[6])
				});
			} else {
				return 1;
			}
		}
	},
	'issueOrder' : function(src, dest, numShip) {
		this.orders.push({
			'src' : parseInt(src),
			'dest' : parseInt(dest),
			'numShip' : parseInt(numShip)
		});
	},
	'finishTurn' : function() {
		for ( var i = 0, len = this.orders.length; i < len; ++i) {
			var order = this.orders[i];
			fs.writeSync(process.stdout.fd, '' + order.src + ' ' + order.dest
					+ ' ' + order.numShip + '\n');
		}
		this.orders = [];
		fs.writeSync(process.stdout.fd, 'go\n');
		//process.stdout.flush();
	},
	'log' : function(msg) {
		fs.writeSync(process.stderr.fd, msg + '\n');
	}
};