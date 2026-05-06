<?php
    include 'db_connection.php';
    $conn = OpenCon();

    //query for sorting
    $sort = $_GET['sort'] ?? 'id';
    $order = $_GET['order'] ?? 'DESC';
    
    //Sorting and 
    $allowedSorts = ['id', 'start', 'total_time', 'completed', 'to_toilet', 'on_toilet', 'to_bed'];
    if (!in_array($sort, $allowedSorts)) $sort = 'id';
    $order = ($order === 'ASC') ? 'ASC' : 'DESC';

    function toggleOrder($currentSort, $column, $currentOrder) {
    if ($currentSort === $column) {
        return $currentOrder === 'ASC' ? 'DESC' : 'ASC';
    }
    return 'ASC'; // default when switching column
    }

    function formatTime($seconds) {
        $minutes = floor($seconds / 60);
        $secs = $seconds % 60;

        return sprintf("%d:%02d", $minutes, $secs);
    }

    //main data query
    $tableResult = $conn->query("SELECT * FROM toilet_visits ORDER BY $sort $order");

    //Usefull stats
    $count = $conn->query("SELECT COUNT(*) AS count FROM toilet_visits")->fetch_assoc()['count'];
    $avg = $conn->query("SELECT AVG(total_time) AS avg FROM toilet_visits")->fetch_assoc()['avg'];
?>
<!DOCTYPE html>
<html>
<head>
    <title>Toilet Visits</title>
    <link rel="stylesheet" href="style.css">
</head>

<body>
<h1>Toilet Visits</h1>
<p class="page-sub">Showing <?= $count ?> total records</p>

<div class="stats-row">
    <div class="stat-card">
        <div class="stat-label">Total visits</div>
        <div class="stat-value"><?= $count ?></div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Avg duration</div>
        <div class="stat-value"><?= formatTime(round($avg)) ?></div>
    </div>
</div>

<div class="table-container">
<table>
<thead>
<tr>
    <th><a href="?sort=id&order=<?= toggleOrder($sort, 'id', $order) ?>">ID</a></th>
    <th><a href="?sort=start&order=<?= toggleOrder($sort, 'start', $order) ?>">Start</a></th>
    <th><a href="?sort=total_time&order=<?= toggleOrder($sort, 'total_time', $order) ?>">Total time</a></th>
    <th><a href="?sort=completed&order=<?= toggleOrder($sort, 'completed', $order) ?>">Completed</a></th>
    <th><a href="?sort=to_toilet&order=<?= toggleOrder($sort, 'to_toilet', $order) ?>">To toilet</a></th>
    <th><a href="?sort=on_toilet&order=<?= toggleOrder($sort, 'on_toilet', $order) ?>">On toilet</a></th>
    <th><a href="?sort=to_bed&order=<?= toggleOrder($sort, 'to_bed', $order) ?>">To bed</a></th>
</tr>
</thead>
<tbody>
<?php
if ($tableResult->num_rows > 0) {
    while ($row = $tableResult->fetch_assoc()) {
        $isLong = $row['total_time'] > 600; // flag visits over 10 min
        echo "<tr>";
        echo "<td>#" . htmlspecialchars($row["id"]) . "</td>";
        echo "<td>" . date("d M Y H:i", strtotime($row["start"])) . "</td>";
        $tdClass = $isLong ? ' class="long-visit"' : '';
        echo "<td$tdClass>" . formatTime($row["total_time"]) . "</td>";
        $done = $row["completed"] ? '<span class="completed">✓ Yes</span>' : '<span class="incomplete">✗ No</span>';
        echo "<td>$done</td>";
        echo "<td>" . formatTime($row["to_toilet"]) . "</td>";
        echo "<td>" . formatTime($row["on_toilet"]) . "</td>";
        echo "<td>" . formatTime($row["to_bed"]) . "</td>";
        echo "</tr>";
    }
}
?>
</tbody>
</table>
</div>
</body>
</html>

<?php
    // Your code here
CloseCon($conn);
?>