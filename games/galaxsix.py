#!/usr/bin/env python

from random import randrange, choice, shuffle, randint, seed, random
from math import sqrt
from collections import deque, defaultdict

from fractions import Fraction
import operator
from game import Game
from copy import deepcopy
try:
    from sys import maxint
except ImportError:
    from sys import maxsize as maxint
	
STAYING_ALIVE_BONUS = 2

class GalaxSix(Game):
    def __init__(self, options=None):
        # setup options
        self.map_text = options['map']
        self.turns = int(options['turns'])
        self.loadtime = int(options['loadtime'])
        self.turntime = int(options['turntime'])
	self.cutoff =''
	self.planets = []
	self.fleets = []
        self.turn = 0
	self.players = dict()
		
        self.parse_map(self.map_text)

        # used to calculate the turn when the winner took the lead
        self.winning_bot = None
        self.winning_turn = 0
        # used to calculate when the player rank last changed
        self.ranking_bots = None
        self.ranking_turn = 0
                
        # initialize scores
        # points start at # of hills to prevent negative scores
        self.score = [1]*self.num_players
        self.bonus = [0]*self.num_players
        self.score_history = [[s] for s in self.score]

        # used to give a different ordering of players to each player
        #   initialized to ensure that each player thinks they are player 0
        self.switch = [[None]*self.num_players + list(range(-5,0)) for i in range(self.num_players)]
        for i in range(self.num_players):
            self.switch[i][i] = 0

        # the engine may kill players before the game starts and this is needed to prevent errors
        self.orders = [[] for i in range(self.num_players)]

    def distance(self, pid_1, pid_2):
        """ Returns distance between x and y squared """
	p1 = self.planets[pid_1]
	p2 = self.planets[pid_2]
        d_row = abs(p1.x - p2.x)
        d_col = abs(p1.y - p2.y)
        return d_row**2 + d_col**2

    def parse_map(self, map_text):
        """ Parse the map_text into a more friendly data structure 
		E 11.014548 9.362856 1 363 2
		M 5.518446 18.725713 1 505
		M 16.510650 0.000000 2 158
		E 18.571299 14.374196 1 190 2
		E 3.457797 4.351517 1 248 2
		E 10.563623 5.157520 2 39 2
	"""

        for line in map_text.split('\n'):
            line = line.strip()
            # ignore blank lines and comments
            if not line:
                continue
	    line = line.split("#")[0]
            key, value = line.split(' ', 1)
	    p = value.split(' ')
	    id = 1
            if key == 'E':
                self.planets.append(EconomicPlanet(id, p[0], p[1], p[2], p[3], p[4]))
            elif key == 'M':
                self.planets.append(MilitaryPlanet(id, p[0], p[1], p[2], p[3]))
	    id += 1
 
	    for p in self.planets:
	        if not p.owner in self.players:
		    self.players[p.owner] = []
		    self.players[p.owner].append(p)

	del self.players[0]    
	self.num_players = len(self.players)
		
    def parse_orders(self, player, lines):
        """ Parse orders from the given player

            Orders must be of the form: source_id target_id num_ships
        """
        valid = []
        ignored = []
        invalid = []

        for line in lines:
            line = line.strip().lower()
            # ignore blank lines and comments
            if not line or line[0] == '#':
                continue

            data = line.split()
            # validate data format
	    if len(data) != 3:
	        invalid.append((line, 'incorrectly formatted order'))
                continue

	    source, target, ships = data

            # validate the data types
            try:
                source_id = int(source)
		target_id = int(target)
		num_ships = int(ships)
            except ValueError:
                invalid.append((line,'invalid data - source target and ships must be integer'))
                continue

            # this order can be parsed
            valid.append(data)

        return valid, ignored, invalid

    def validate_orders(self, player, lines, orders, ignored, invalid):
        """ Validate orders from a given player
            source_id must be a military planet belonging to the player
	    num_ships must be lower or equal than the number of ships on the planet
        """
        valid = []
        valid_orders = []
        for line, order in zip(lines, orders):
	    source_id = order[0]
	    target_id = order[1]

            try:
		if self.planets[source_id].owner != player:
		    invalid.append((line,'planet not belonging to player'))
		    continue
            except IndexError:
                invalid.append((line,'invalid source planet'))
                continue

	    try:
		self.planets[target_id]
            except IndexError:
                invalid.append((line,'invalid target planet'))
                continue
					
	    source_planet = self.planets[source_id]
	    if not isinstance(source_planet, MilitaryPlanet):
		invalid.append((line,'source planet not military'))
		continue
			
	    if source_planet.num_ships < order[2]:
                ignored.append((line,'not enough ships on source planet'))
                continue

            # this order is valid!
            valid.append(order)

        return valid, ignored, invalid

    def do_orders(self):
        """ Create fleets for each player order
	"""
	for player in self.players:
	    for order in self.orders[player]:
		source_id = order[0]
		target_id = order[1]
		num_ships = order[2]
		distance = self.distance(source_id, target_id)
		p = self.planets[source_id] 
		self.fleets.append(Fleet(p.owner, num_ships, source_id, target_it, distance, distance))

    def do_timestep(self):
	""" All Economic planets will produce ships
	    All Fleets move forward
	    Resolve all battles on planets
        """
        for p in self.planets:
	    if isinstance(p, EconomicPlanet) and p.owner > 0:
	        military_planets = self.military_planets_for_player(p.owner)
		if (len(military_planets) > 0):
		    distance = maxint
		    target = military_planets[0]
		    for m in military_planets:
			if (self.distance(m.id, p.id) < distance):
			    distance = self.distance(m.id, p.id)
			    target = m
			    self.fleets.append(Fleet(p.owner, p.growth_rate, p.id, target.id, distance, distance))

	for f in self.fleets:
	    f.do_timestep();

	for p in self.planets:
	    self.do_fight(p);

    def do_fight(self, p):
        battleships = dict();
        remaining_fleets = []
        battleships[p.owner] = p.num_ships
        for f in self.fleets:
            if f.destination_planet == p.id and f.turns_remaining == 0:
	        if not p.owner in battleships:
		    battleships[p.owner] = 0
		    battleships[p.owner] += f.num_ships
		else:
		    remaining_fleets.append(f);

	self.fleets = remaining_fleets;

	if len(battleships) == 0:
	    # No fight
	    return
	elif len(battleships) == 1:
	    # Only one player - No fight
	    p.num_ships = battleships[p.owner]
	    return

	max_ships = -1
	max_owner = -1
	second_ships = -1

	for k, v in zip(battleships.keys(), battleships.values()):
	    if v > max_ships:
		max_ships = v
		max_owner = k

	for k, v in zip(battleships.keys(), battleships.values()):
	    if v > second_ships and k != max_owner:
		second_ships = v

	p.num_ships = max_ships - second_ships
	if max_ships != second_ships:
	    # Biggest fleet is new owner (maybe doesn't change)
	    p.owner = max_owner
	#else:	
	    # Mutually assured destruction --> Owner doesn't change, ships are 0
		
    # Common functions for all games

    def is_rank_stabilized(self):
        """ Determine if the rank can be changed by bots with hills.

            Determines if there are enough hills left for any player to overtake
            another in score.  Only consider bots with remaining hills.
            Those without hills will not be given the opportunity to overtake
        """
        return False

    def military_planets_for_player(self, player):
	return [p for p in self.planets if isinstance(p, MilitaryPlanet) and p.owner == player]
		
    def remaining_players(self):
        """ Return the players still alive """
        return [p for p in range(self.num_players) if self.is_alive(p)]

    def get_scores(self, player=None):
        """ Gets the scores of all players

            Used by engine for ranking
        """
        if player is None:
            return self.score
        else:
            return self.order_for_player(player, self.score)

    def order_for_player(self, player, data):
        """ Orders a list of items for a players perspective of player #

            Used by engine for ending bot states
        """
        s = self.switch[player]
        return [None if i not in s else data[s.index(i)] for i in range(max(len(data),self.num_players))]

    def game_over(self):
        """ Determine if the game is over
	    Used by the engine to determine when to finish the game.
            A game is over when there are no players remaining, or a single
             winner remaining.
        """
        if len(self.remaining_players()) < 1:
            self.cutoff = 'extermination'
            return True
        if len(self.remaining_players()) == 1:
            self.cutoff = 'lone survivor'
            return True
        return False

    def kill_player(self, player):
        """ Used by engine to signal that a player is out of the game """
	for p in self.planets:
	    if p.owner == player:
		p.owner = 0

	for f in self.fleets:
	    if f.owner == player:
		f.owner = 0
		f.num_ships = 0
		f.turns_remaining = 0
		
    def start_game(self):
        """ Called by engine at the start of the game """

    def finish_game(self):
        """ Called by engine at the end of the game """
        # survivors get a bonus
        players = self.remaining_players()
	for player in range(self.num_players):
	    self.score[player] += STAYING_ALIVE_BONUS

        self.calc_significant_turns()
        
        # check if a rule change lengthens games needlessly
        if self.cutoff is None:
            self.cutoff = 'turn limit reached'

    def start_turn(self):
        """ Called by engine at the start of the turn """
        self.turn += 1

    def finish_turn(self):
        """ Called by engine at the end of the turn """
        self.do_orders()
	self.do_timestep()

        # record score in score history
        for i, s in enumerate(self.score):
            if self.is_alive(i):
                self.score_history[i].append(s)
            elif s != self.score_history[i][-1]:
                # the score has changed, probably due to a dead bot losing a hill
                # increase the history length to the proper amount
                last_score = self.score_history[i][-1]
                score_len = len(self.score_history[i])
                self.score_history[i].extend([last_score]*(self.turn-score_len))
                self.score_history[i].append(s)

        self.calc_significant_turns()

    def calc_significant_turns(self):
        ranking_bots = [sorted(self.score, reverse=True).index(x) for x in self.score]
        if self.ranking_bots != ranking_bots:
            self.ranking_turn = self.turn
        self.ranking_bots = ranking_bots

        winning_bot = [p for p in range(len(self.score)) if self.score[p] == max(self.score)]
        if self.winning_bot != winning_bot:
            self.winning_turn = self.turn
        self.winning_bot = winning_bot

    def get_state(self):
        """ Get all state changes

            Used by engine for streaming playback
        """
        result = []
	for planet in self.planets: 
	    result.append(str(planet))
	    for fleet in self.fleets: 
		result.append(str(fleet))
        return '\n'.join(' '.join(map(str,s)) for s in result)

    def get_player_start(self, player=None):
        """ Get game parameters visible to players

            Used by engine to send bots startup info on turn 0
        """
        result = []
        result.append(['turn', 0])
        result.append(['loadtime', self.loadtime])
        result.append(['turntime', self.turntime])
        result.append(['turns', self.turns])
        result.append([]) # newline
	for row in self.map_text:
	    result.append(row)
        return '\n'.join(' '.join(map(str,s)) for s in result)

    def get_player_state(self, player):
        """ Get state changes visible to player

            Every player sees everything in this game
        """
	return self.get_state()

    def is_alive(self, player):
        """ Determine if player is still alive
            Used by engine to determine players still in the game
        """
	for p in self.planets: 
	    if p.owner == player:
		return True
        return False

    def get_error(self, player):
        """ Returns the reason a player was killed
            Used by engine to report the error that kicked a player
            from the game
        """
        return ''

    def do_moves(self, player, moves):
        """ Called by engine to give latest player orders """
        valid, ignored, invalid = self.parse_orders(player, moves)
        valid, ignored, invalid = self.validate_orders(player, moves, valid, ignored, invalid)
        self.orders[player] = valid
        return valid, ['%s # %s' % ignore for ignore in ignored], ['%s # %s' % error for error in invalid]

    def get_scores(self, player=None):
        """ Gets the scores of all players

            Used by engine for ranking
        """
        return self.score

    def get_stats(self):
        """ Get current ant counts
            Used by engine to report stats
        """
        stats = {}
        stats['winning'] = self.winning_bot
        stats['w_turn'] = self.winning_turn
        stats['ranking_bots'] = self.ranking_bots
        stats['r_turn'] = self.ranking_turn
        stats['score'] = self.score
        stats['s_alive'] = [1 if self.is_alive(player) else 0 for player in range(self.num_players)]
        stats['climb?'] = []
        stats['max_score'] = {}
        for player in range(self.num_players):
            stats['max_score'][player] = max_score
#                stats['min_score_%s' % player] = {}
#                        stats['min_score_%s' % player][opponent] = min_score
            stats['climb?'].append(0)
        return stats

    def get_replay(self):
        """ Return a summary of the entire game

            Used by the engine to create a replay file which may be used
              to replay the game.
        """
        replay = {}
        # required params
        replay['revision'] = 3
        replay['players'] = self.num_players

        # optional params
        replay['loadtime'] = self.loadtime
        replay['turntime'] = self.turntime
        replay['turns'] = self.turns

        # map
        replay['map'] = {}
        replay['map']['data'] = self.get_state()

        # scores
        replay['scores'] = self.score_history
        replay['bonus'] = self.bonus
        replay['winning_turn'] = self.winning_turn
        replay['ranking_turn'] = self.ranking_turn
        replay['cutoff'] =  self.cutoff

        return replay

class Fleet:
    def __init__(self, owner, num_ships, source_planet, destination_planet, total_trip_length, turns_remaining):
	self.owner = owner
	self.num_ships = num_ships
	self.source_planet = source_planet
	self.destination_planet = destination_planet
	self.total_trip_length = total_trip_length
	self.turns_remaining = turns_remaining
		
    def __str__(self): 
	### F for fleet, owner, num_ships, source planet id, target planet id, total_trip_length, remaining_turns ###
	return "F %d %d %d %d %d %d" % (self.owner, self.num_ships, self.source_planet, self.destination_planet, self.total_trip_length, self.turns_remaining)

    def do_timestep(self):
	self.turns_remaining -= 1
	if self.turns_remaining < 0:
	    self.turns_remaining = 0
	
class Planet:
    def __init__(self, id, x, y, owner, num_ships):
	self.id = id
	self.owner = int(owner)
	self.num_ships = int(num_ships)
	self.x = float(x)
	self.y = float(y)

class EconomicPlanet(Planet): 
    def __init__(self, id, x, y, owner, num_ships, growth_rate):
	Planet.__init__(self, id, x, y, owner, num_ships)
	self.growth_rate = int(growth_rate)

	def __str__(self):
	    return "E %f %f %d %d %d" % (self.x, self.y, self.owner, self.num_ships, self.growth_rate)

class MilitaryPlanet(Planet): 
    def __init__(self, id, x, y, owner, num_ships):
	Planet.__init__(self, id, x, y, owner, num_ships)

    def __str__(self):
	return "M %f %f %d %d" % (self.x, self.y, self.owner, self.num_ships)