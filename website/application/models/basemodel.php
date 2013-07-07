<?php 
Class Basemodel extends CI_Model {
	
	var $resultAsArray = FALSE;

	function __construct() {
		// Call the Model constructor
		parent::__construct();
	}
	
	function getTableName() {
		// Implement this
	}

	/**
	 * Récupère toutes les lignes d'une table (et tous les champs)
	 * 
	 * @param int $limit
	 * @return $query->result():
	 */
	function getAll($limit = -1) {
		// Ajout de la limite
		if ($limit > 0) {
			$this->db->limit($limit);
		}

		// Lancement de la requête
		$query = $this->db->get($this->getTableName());
		if ($query->num_rows())  {
			if ($this->resultAsArray) {
				return $query->result_array();
			} else {
				return $query->result();
			}
		}
		return array();
	}

	/**
	 * Récupère toutes les lignes d'une table pour affichage combo
	 * 
	 * @param $id_field nom du champ servant d'ID
	 * @return array($id_field => $value_field)
	 */
	function getAllForCombo($id_field, $value_field) {
		// Ajout du select
		$this->db->select($id_field.', '.$value_field);
		
		// Lancement de la requête
		$query = $this->db->get($this->getTableName());
		if ($query->num_rows())  {
			$results = $query->result();
			
			$resultArray = array();
			foreach ($results as $result) {
				$resultArray[$result->$id_field] = $result->$value_field;
			}
			
			return $resultArray;
		}
		return array();
	}

	/**
	 * Recherche dans une table.
	 * Permet de définir les colonnes et les conditions
	 *
	 * @param string $select [default '']
	 * @param array(array()) $clauses [default array()]
	 * @param int $limit [default -1]
	 * @return $query->result()
	 */
	function search($select = '', $clauses = array(), $limit = -1) {
		// Ajout de la clause select
		if ($select != '') {
			$this->db->select($select);
		}
		
		// Ajout des conditions
		if (is_array($clauses) && count($clauses) > 0) {
			foreach ($clauses as $clause) {
				if (isset($clause[2])) {
					$this->db->or_where($clause[0], $clause[1]);
				} else {
					$this->db->where($clause[0], $clause[1]);
				}
			}
		}
		
		// Ajout de la limite
		if ($limit > 0) {
			$this->db->limit($limit);
		}
		
		// Lancement de la requête
		$query = $this->db->get($this->getTableName());
		if ($query->num_rows())  {
			if ($this->resultAsArray) {
				return $query->result_array();
			} else {
				return $query->result();
			}
		}
		return array();
	}

	/**
	 * Count dans une table.
	 *
	 * @param array(array()) $clauses [default array()]
	 * @return int
	 */
	function count($clauses = array()) {
		// Ajout des conditions
		if (is_array($clauses) && count($clauses) > 0) {
			foreach ($clauses as $clause) {
				if (isset($clause[2])) {
					$this->db->or_where($clause[0], $clause[1]);
				} else {
					$this->db->where($clause[0], $clause[1]);
				}
			}
		}
		
		// Lancement de la requête
		return $this->db->count_all();
	}
	
	/**
	 * Insert d'une donnée en base.
	 * Utiliser la classe courante pour les donnée.
	 */
	function insert() {
        $this->db->insert($this->getTableName(), $this);
	}

	/**
	 * Mise à jour de la donnée spécifiée.
	 * 
	 */
	function update($idField, $idValue, $data) {
        $this->db->update($this->getTableName(), $data, array($idField => $idValue));
	}

	/**
	 * Suppression de la donnée spécifiée.
	 */
	function delete($idField, $idValue) {
		$this->db->delete($this->getTableName(), $this, array($idField => $idValue));
	}
}
