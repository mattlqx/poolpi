<?php header('Expires: '.gmdate('D, d M Y H:i:s \G\M\T', time() + (60 * 60))); ?>
<html>
<head>
<title>Pool Temperature</title>
</head>
<body>
<h1>Daily</h1>
<img src="temperature.php?lookback=86400"><br />
<img src="temperature.php?lookback=86400&probe_only"><br />

<h1>Weekly</h1>
<img src="temperature.php?lookback=604800"><br />
<img src="temperature.php?lookback=604800&probe_only"><br />

<h1>Monthly</h1>
<img src="temperature.php?lookback=2419200"><br />
<img src="temperature.php?lookback=2419200&probe_only"><br />

<h1>Yearly</h1>
<img src="temperature.php?lookback=31449600"><br />
<img src="temperature.php?lookback=31449600&probe_only"><br />

</body>
</html>
