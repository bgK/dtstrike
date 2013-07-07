<?php 
Class Game_playermodel extends Basemodel {
 
  var $game_id = -1; // int(11)
  var $user_id = -1; // int(11)
  var $submission_id = -1; // int(11)
  var $player_id = -1; // int(11)
  var $errors = ''; // varchar(1024)
  var $status = ''; // varchar(255)
  var $game_rank = -1; // int(11)
  var $game_score = -1; // int(11)
  var $rank_before = -1; // int(11)
  var $rank_after = -1; // int(11)
  var $mu_before = ''; // float
  var $mu_after = ''; // float
  var $sigma_before = ''; // float
  var $sigma_after = ''; // float
  var $valid = ''; // tinyint(1)
 
  function __construct() {
    // Call the BaseModel constructor
    parent::__construct();
  }
 
  function getTableName() {
    return 'game_player';
  }
 
} 
 