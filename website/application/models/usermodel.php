<?php 
Class Usermodel extends Basemodel {
 
  var $user_id = -1; // int(11)
  var $username = ''; // varchar(128)
  var $password = null; // varchar(256)
  var $reset = null; // varchar(256)
  var $email = ''; // varchar(256)
  var $activation_code = ''; // varchar(256)
  var $org_id = -1; // int(11)
  var $bio = ''; // varchar(4096)
  var $country_code = ''; // varchar(8)
  var $created = ''; // datetime
  var $activated = 0; // tinyint(1)
  var $shutdown_date = ''; // datetime
  var $max_game_id = -1; // int(11)
 
  function __construct() {
    // Call the BaseModel constructor
    parent::__construct();
  }
 
  function getTableName() {
    return 'user';
  }
 
} 
 
