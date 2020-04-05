<?php

function get_sun_data($datestamp) {
  return json_decode(exec("./sunrise.py $datestamp"));
}

function get_config() {
  return json_decode(exec("./dump_config.py"), true);
}

// Bail if etag matches (of same minute)
$etag = md5(time() - time() % 60);
if (trim($_SERVER['HTTP_IF_NONE_MATCH']) == $etag) {
  header("HTTP/1.1 304 Not Modified");
  exit;
}

chdir(realpath(dirname(__FILE__).'/..'));

// Define range via query string
$lookback = isset($_GET['lookback']) && is_numeric($_GET['lookback']) ? min($_GET['lookback'], 29030400) : 604800;
$start = isset($_GET['start']) && is_numeric($_GET['start']) ? max(time() - (60 * 60 * 24 * 365), $_GET['start']) : time();
$probe_only = isset($_GET['probe_only']);
$show_cmd = isset($_GET['show_cmd']);

$sun_data = [];
$vrules = [];

// Sunrise and sunset markers
$cur_time = time();
if ($lookback <= 3600000) {
  for ($offset = 0; $offset <= $lookback; $offset += 86400) {
    $sun_data[] = get_sun_data($cur_time - $offset);
  }
  foreach ($sun_data as $data) {
    if ($data->sunrise < $cur_time) {
      $vrules[] = 'VRULE:'.$data->sunrise.'#ffa500';
    }
    if ($data->sunset < $cur_time) {
      $vrules[] = 'VRULE:'.$data->sunset.'#ffa500';
    }
    if ($data->peak < $cur_time && $lookback <= 604800) {
      $vrules[] = 'VRULE:'.$data->peak.'#ff0000';
    }
  }
}

// Graphing
$config = get_config();
$tmpfile = tempnam("/tmp", "pooltemp");
$rrd_graph = "rrdtool graph $tmpfile -w 785 -h 240 -a PNG --slope-mode --start -$lookback --end $start --vertical-label \"temperature (°F)\" ";
$rrd_defs = [];
$color = array_key_exists('color_start', $config) == true ? $config['color_start'] : 0xff0000;
foreach ($config['temperature_probes'] as $probe_data) {
  $probe = array_keys($probe_data)[0];
  $color_string = sprintf("%06x", $color);
  $color = abs($color >> (array_key_exists('color_offset', $config) == true ? $config['color_offset'] : 12));

  if ($probe_only && $probe != 'probe') {
    continue;
  }

  $rrd_defs[] = "  DEF:$probe=temperature.rrd:$probe:AVERAGE LINE2:$probe#{$color_string}:\"$probe\" \
    VDEF:{$probe}max={$probe},MAXIMUM \
    GPRINT:{$probe}max:\"Max\:  %5.2lf°F\" \
    VDEF:{$probe}min={$probe},MINIMUM \
    GPRINT:{$probe}min:\"Min\:  %5.2lf°F\" \
    VDEF:{$probe}cur={$probe},LAST \
    GPRINT:{$probe}cur:\"Cur\:  %5.2lf°F\l\" \
    \\\n";
}
$rrd_graph .= implode(" \\\n ", $rrd_defs)." \\\n".implode(" \\\n  ", $vrules);

if ($show_cmd) {
  header('Content-Type: plain/text');
  echo $rrd_graph;
  exit(0);
}

header('Content-Type: image/png');

exec($rrd_graph);

header('Etag: ' . $etag);
header('Content-Length: ' . filesize($tmpfile));
header('Access-Control-Allow-Origin: http://ask-ifr-download.s3.amazonaws.com');

readfile($tmpfile);
unlink($tmpfile);
?>
