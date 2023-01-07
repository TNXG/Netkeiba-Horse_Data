<?php
$horseid = $_GET['id'];
$data = exec('python ./core/index.py "' . $horseid . '"');
// 设置响应头json
header('Content-Type: application/json');
echo iconv('gbk', 'utf-8', $data);
