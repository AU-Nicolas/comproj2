<?php
    include 'db_connection.php';
    $conn = OpenCon();

    //query for sorting
    $sort = $_GET['sort'] ?? 'start';
    $order = $_GET['order'] ?? 'DESC';
    
    //Sorting and 
    $allowedSorts = ['start', 'total_time', 'completed', 'to_toilet', 'on_toilet', 'to_bed'];
    if (!in_array($sort, $allowedSorts)) $sort = 'start';
    $order = ($order === 'ASC') ? 'ASC' : 'DESC';

    function toggleOrder($currentSort, $column, $currentOrder) {
    if ($currentSort === $column) {
        return $currentOrder === 'ASC' ? 'DESC' : 'ASC';
    }
    return 'ASC'; // default when switching column
    }

    //main data query
    $tableResult = $conn->query("SELECT * FROM toilet_visits ORDER BY $sort $order");

    //Usefull stats
    $count = $conn->query("SELECT COUNT(*) AS count FROM toilet_visits")->fetch_assoc()['count'];
    $avg = $conn->query("SELECT AVG(total_time) AS avg FROM toilet_visits")->fetch_assoc()['avg'];
?>
<!DOCTYPE html>
<html>
<body>

<h1>Toilet Visits</h1>

<table border="1">
<tr>
    <th>ID</th>
    <th>
        <a href="?sort=start&order=<? = toggleOrder($sort, 'start', $order) ?>"> Start</a>
    </th>
    <th>
        <a href="?sort=total_time&order=<? = toggleOrder($sort, 'total_time', $order) ?>"> Total Time</a>
    </th>
    <th>
        <a href="?sort=Completed&order=<? = toggleOrder($sort, 'completed', $order) ?>"> Completed</a>
    </th>
    <th>
        <a href="?sort=to_toilet&order=<? = toggleOrder($sort, 'to_toilet', $order) ?>"> To Toilet</a>
    </th>
    <th>
        <a href="?sort=on_toilet&order=<? = toggleOrder($sort, 'on_toilet', $order) ?>"> On Toilet</a>
    </th>
    <th>
        <a href="?sort=to_bed&order=<? = toggleOrder($sort, 'to_bed', $order) ?>"> To Bed</a>
    </th>
</tr>

<?php
if ($tableResult->num_rows > 0) {
    while ($row = $tableResult->fetch_assoc()) {
        echo "<tr>";
        echo "<td>" . htmlspecialchars($row["id"]) . "</td>";
        echo "<td>" . htmlspecialchars($row["start"]) . "</td>";
        echo "<td>" . htmlspecialchars($row["total_time"]) . "</td>";
        echo "<td>" . htmlspecialchars($row["completed"]) . "</td>";
        echo "<td>" . htmlspecialchars($row["to_toilet"]) . "</td>";
        echo "<td>" . htmlspecialchars($row["on_toilet"]) . "</td>";
        echo "<td>" . htmlspecialchars($row["to_bed"]) . "</td>";
        echo "</tr>";
    }
}
?>

</table>

</body>
</html>

<?php
    // Your code here
CloseCon($conn);
?>