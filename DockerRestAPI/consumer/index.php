<!DOCTYPE html>
<html>
<head>
    <title>CIS 322 REST-api demo: Brevets list</title>
</head>
<body>
    <h1>List of Brevets</h1>
    <nav>
        <ul>
            <li><a href="?list=all">List All</a></li>
            <li><a href="?list=open">List Open Only</a></li>
            <li><a href="?list=close">List Close Only</a></li>
        </ul>
    </nav>
    <ul>
        <?php
        $list = isset($_GET['list']) ? $_GET['list'] : 'all';
        $url = 'http://web:5000/';
        
        if ($list == 'open') {
            $url .= 'listOpenOnly/json';
        } elseif ($list == 'close') {
            $url .= 'listCloseOnly/json';
        } else {
            $url .= 'listAll/json';
        }

        $json = file_get_contents($url);
        if ($json === FALSE) {
            echo "<li>Failed to fetch data from web service</li>";
            error_log("Failed to fetch data from $url");
        } else {
            $obj = json_decode($json);
            $brevets = $obj->brevets;
            foreach ($brevets as $b) {
                $open = isset($b->open) ? $b->open : "";
                $close = isset($b->close) ? $b->close : "";
                $brevet_dist_km = isset($b->brevet_dist_km) ? $b->brevet_dist_km : "";
                $km = isset($b->km) ? $b->km : "";
                $location = isset($b->location) ? $b->location : "";
                $miles = isset($b->miles) ? $b->miles : "";
                echo "<li>Brevet Distance: $brevet_dist_km, Control Distance: $km, Open: $open, Close: $close, Location: $location, Miles: $miles</li>";
            }
        }
        ?>
    </ul>
</body>
</html>