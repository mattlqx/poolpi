<?php

function get_sun_data($datestamp) {
  return json_decode(exec("./sunrise.py $datestamp"));
}

chdir(realpath(dirname(__FILE__).'/..'));

// Define range via query string
$lookback = isset($_GET['lookback']) && is_numeric($_GET['lookback']) ? min($_GET['lookback'], 29030400) : 604800;
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
$rrd_graph = "rrdtool graph $tmpfile -w 785 -h 240 -a PNG --slope-mode --start -$lookback --end now --vertical-label \"temperature (°F)\" \
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
header('Content-Length: ' . filesize($tmpfile));
header('Expires: '.gmdate('D, d M Y H:i:s \G\M\T', time() + 60));

readfile($tmpfile);
unlink($tmpfile);
?>
