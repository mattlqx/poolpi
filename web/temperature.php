<?php

function get_sun_data($datestamp) {
  return json_decode(exec("./sunrise.py $datestamp"));
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
$tmpfile = tempnam("/tmp", "pooltemp");
$rrd_graph = "rrdtool graph $tmpfile -w 785 -h 240 -a PNG --slope-mode --start -$lookback --end $start --vertical-label \"temperature (°F)\" \
  DEF:temp=temperature.rrd:probe:AVERAGE LINE2:temp#0000ff:\"probe\" \
  VDEF:probemax=temp,MAXIMUM \
  GPRINT:probemax:\"  Max\:  %5.2lf°F\" \
  VDEF:probemin=temp,MINIMUM \
  GPRINT:probemin:\"Min\:  %5.2lf°F\" \
  VDEF:probecur=temp,LAST \
  GPRINT:probecur:\"Cur\:  %5.2lf°F\l\" \\\n";
if (!$probe_only) {
  $rrd_graph .= "  DEF:temp2=temperature.rrd:outdoor:AVERAGE LINE2:temp2#ff0000:\"outside\" \
  VDEF:outsidemax=temp2,MAXIMUM \
  GPRINT:outsidemax:\"Max\:  %5.2lf°F\" \
  VDEF:outsidemin=temp2,MINIMUM \
  GPRINT:outsidemin:\"Min\:  %5.2lf°F\" \
  VDEF:outsidecur=temp2,LAST \
  GPRINT:outsidecur:\"Cur\:  %5.2lf°F\l\" \
\\\n";
}
$rrd_graph .= implode(" \\\n  ", $vrules);

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
