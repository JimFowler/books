<?php
////////////////////////////////////////////////////////////////////
class MySQLResultSet implements Iterator{
  //data members
  private $strSQL;
  private $databasename;
  private $connection;
  private $result;
  private $valid;
  private $currentrow;
  private $key;
  //programmer defined error numbers
  //in range not used by MySQL
  const INDETERMINATE_TOTAL_NUMBER = 5001;
  const UNNECESSARY_SQL_CALC_FOUND_ROWS = 5002;
  const NOT_SELECT_QUERY = 5003;
////////////////////////////////////////////////////////////////////
//constructor
////////////////////////////////////////////////////////////////////
  public function __construct( $strSQL, $databasename, $connection ){
    $this->strSQL = $strSQL;
    $this->connection = $connection;
    $this->databasename = $databasename;
    if(!mysql_selectdb($databasename, $connection)){
      throw new MySQLException(mysql_error(), mysql_errno());
    }
    if(!$this->result = mysql_query($strSQL, $connection)){
      throw new MySQLException(mysql_error(), mysql_errno());
    }
    //check if contains SQL_CALC_FOUND_ROWS
    if (stristr($strSQL,"SQL_CALC_FOUND_ROWS")){
      $msg = "No need to use SQL_CALC_FOUND_ROWS.";
      throw new MySQLException($msg, self::UNNECESSARY_SQL_CALC_FOUND_ROWS);
    }
    //initialize values (not necessary for foreach)
    $this->rewind();
  }
////////////////////////////////////////////////////////////////////
//destructor
////////////////////////////////////////////////////////////////////
  public function __destruct(){
    $this->close();
  }
////////////////////////////////////////////////////////////////////
// public methods
////////////////////////////////////////////////////////////////////  
  public function getDatabaseName(){
    return $this->databasename;
  }
////////////////////////////////////////////////////////////////////
  public function getNumberColumns(){
    return mysql_num_fields($this->result);
  }
////////////////////////////////////////////////////////////////////
//For select queries only
////////////////////////////////////////////////////////////////////
  public function getNumberRows(){
    return mysql_num_rows($this->result);
  }
////////////////////////////////////////////////////////////////////
  public function getInsertId(){
    return mysql_insert_id( $this->connection); 
  }
////////////////////////////////////////////////////////////////////
//Calculate total number of records if a limit clause present
//Useful for calculating number of pages in versions < 4
//Unreliable results if DISTINCT used
////////////////////////////////////////////////////////////////////
  public function getUnlimitedNumberRows(){
    $number = 0;
    $versionnumber = $this->findVersionNumber();
    //only need leftmost number
    $version = substr($versionnumber,0,1);
    //CHECK SELECT
    if (!$this->checkForSelect()){
      $msg = "Illegal method call - not a SELECT query";
      throw new MySQLException($msg, self::NOT_SELECT_QUERY);
    }
    //check for limit clause
    $tempsql = strtoupper($this->strSQL);
    $end = strpos($tempsql,"LIMIT");
    if ($end === false){ //no limit clause
      $number = mysql_num_rows($this->result);
    }
    elseif($version < 4){
      $number = $this->countVersionThree($end);
    }else{ //version 4 or higher use SQL_CALC_FOUND_ROWS function
      $number = $this->countVersionFour();
    }
    return $number;
  }
////////////////////////////////////////////////////////////////////
  public function getFieldNames(){
    $fieldnames = array();
    if(isset($this->result)){
      $num = mysql_numfields($this->result);
      for($i = 0; $i < $num; $i++){
        if (!$meta = mysql_fetch_field($this->result, $i)){
          throw new MySQLException(mysql_error(), mysql_errno());
        }else{
          $fieldnames[$i]= $meta->name;
        }
      }
    }
    return $fieldnames;
  }
////////////////////////////////////////////////////////////////////
  public function findVersionNumber(){
    //mysql_get_server_info
    return mysql_get_server_info($this->connection);
  }
////////////////////////////////////////////////////////////////////
//Iterator methods that must be implemented 
////////////////////////////////////////////////////////////////////
  public function current (){
    return $this->currentrow;
  }
////////////////////////////////////////////////////////////////////
  public function key (){
    return $this->key;
  }
////////////////////////////////////////////////////////////////////
  public function next (){
    if($this->currentrow = mysql_fetch_array($this->result, MYSQL_BOTH)){
      $this->valid = true;
      $this->key++;
    }else{
      $this->valid = false;
    }
  }
////////////////////////////////////////////////////////////////////
  public function rewind (){
    if($num = mysql_num_rows($this->result) > 0){
      if(mysql_data_seek($this->result, 0)){
        $this->valid = true;
        $this->key = 0;
        $this->currentrow = mysql_fetch_array($this->result);
      }
    }else{
      $this->valid = false;
    } 
  }
////////////////////////////////////////////////////////////////////
 	public function valid (){
    return $this->valid;
  }
////////////////////////////////////////////////////////////////////
//private methods
////////////////////////////////////////////////////////////////////  
  private function checkForSelect(){
    $bln = true;
    $strtemp = trim(strtoupper($this->strSQL));
    if(substr($strtemp,0,6)!= "SELECT"){
      $bln = false;
    }
    return $bln;  
  }
////////////////////////////////////////////////////////////////////
  private function close(){
    if(isset($this->result)){
      mysql_free_result($this->result);
      unset($this->result);
    }
  }
////////////////////////////////////////////////////////////////////  
  private function countVersionFour(){
    $tempsql = trim($this->strSQL);
    //insert SQL_CALC_FOUND_ROWS
    $insertstr = " SQL_CALC_FOUND_ROWS ";
    //already know it starts with "SELECT"
    $tempsql = substr_replace($tempsql, $insertstr, 6, 1);
    if(!$rs = mysql_query($tempsql, $this->connection)){
      throw new MySQLException(mysql_error(), mysql_errno());
    }
    $tempsql = "SELECT FOUND_ROWS()";
    if(!$rs = mysql_query($tempsql)){
      throw new MySQLException(mysql_error(), mysql_errno());
    }
    $row = mysql_fetch_row($rs);
    $number = $row[0];
    //dispose of $rs
    mysql_free_result($rs);
    return $number;
  }
////////////////////////////////////////////////////////////////////  
  private function countVersionThree($end){
    $tempsql = strtoupper($this->strSQL);
    //check for DISTINCT - will throw things off
    if(!strpos($tempsql,"DISTINCT")){
      //create recordset
      $start = strpos($tempsql,"FROM");
      $numchars = $end-$start;
      $countsql = "SELECT COUNT(*) ";
      $countsql .= substr($this->strSQL, $start, $numchars);
      if(!$rs=mysql_query($countsql, $this->connection)){
        throw new MySQLException( mysql_error(), mysql_errno());
      }
      $row = mysql_fetch_row($rs);
      $number = $row[0];
      //dispose of $rs
      mysql_free_result($rs);
    }else{
      $msg = "Using keyword DISTINCT, ".
         "calculate total number manually.";
      //must use self - not a property
      throw new MySQLException($msg, self::INDETERMINATE_TOTAL_NUMBER);
    }
    return $number;
  }
}//end class
?>
