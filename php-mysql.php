 <?php
$servername = "localhost";
$username = "pi";
$password = "dorques";
$dbname = "mydb";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT seq100, end_time, avg_time FROM run100";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "Sequence Group: " . $row["seq100"]. " - Ending Time: " . $row["end_time"]. "- Group Average: " . $row["avg_time"]. "<br>";
    }
} else {
    echo "0 results";
}
$conn->close();
?> 
