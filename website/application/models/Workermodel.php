<?php 
Class Workermodel extends Basemodel {
 
  var $worker_id = -1; // int(11)
  var $ip_address = ''; // varchar(15)
  var $api_key = ''; // varchar(256)
 
  function __construct() {
    // Call the BaseModel constructor
    parent::__construct();
  }
 
  function getTableName() {
    return 'worker';
  }
 
} 
 
