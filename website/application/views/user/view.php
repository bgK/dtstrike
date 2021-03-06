<style>
.table_label {
	width: 160px;
	padding-top: 5px;
	text-align: right;
}
.table_value {
	padding-top: 5px;
	padding-left: 20px;
}
</style>

<table style="width: 100%">
	<tr>
		<td class="table_label">Username :</td>
		<td class="table_value"><?php echo $user->username; ?></td>
	</tr>
<?php if (verify_user_role($this, "admin", TRUE)) { ?>
	<tr>
		<td class="table_label">E-mail :</td>
		<td class="table_value"><?php echo $user->email; ?></td>
	</tr>
<?php } ?>
	<tr>
		<td class="table_label">Organisation :</td>
		<td class="table_value"><?php echo $user->org_name; ?></td>
	</tr>
	<tr>
		<td class="table_label">Pays :</td>
		<td class="table_value"><?php echo $user->country_name; ?></td>
	</tr>
	<tr>
		<td class="table_label">Bio :</td>
		<td class="table_value"><?php echo nl2br($user->bio, true); ?></td>
	</tr>
	<tr>
		<td class="table_label">Meilleur classement :</td>
		<td class="table_value"><?php echo 'TODO'; ?></td>
	</tr>
	<tr>
		<td class="table_label"></td>
		<td class="table_value"><hr/></td>
	</tr>
	<tr>
		<td class="table_label">Liens :</td>
		<td class="table_value"><?php echo '<a href="' . site_url("game/liste/user_id/".$user->user_id) . '">Voir les matchs de ce joueur</a>'; ?></td>
	</tr>
</table>
