<?php

// All timestamps output are in UTC

chdir(realpath(dirname(__FILE__).'/..'));

$data = array();

list($ts, $probe_temp, $outdoor_temp) = explode(' ', exec("rrdtool fetch temperature.rrd -s -180 -e -60 AVERAGE | tail -n 1"));

$data['probe_temp_f'] = (float)sprintf("%0.02f", $probe_temp);
$data['outdoor_temp_f'] = (float)sprintf("%0.02f", $outdoor_temp);
$data['peak_temp_f'] = null;
$data['peak_temp_time'] = null;

$midnight = time() - (time() % 86400);

exec("rrdtool fetch temperature.rrd -s ".($midnight - 86400)." -e $midnight AVERAGE", $last_day);

foreach ($last_day as $line) {
  if (preg_match("/(\d+): (\d+\.\d+e\+01) (\d+\.\d+e\+01)/", $line, $matches)) {
    $rounded_probe_f = (float)sprintf("%0.02f", $matches[2]);
    if ($rounded_probe_f > $data['peak_temp_f']) {
      $data['peak_temp_f'] = $rounded_probe_f;
      $data['peak_temp_time'] = (int)$matches[1];
    }
  }
}

$json = json_encode($data);

header('Content-Type: application/json');
header('Content-Length: '.strlen($json));

echo $json;
