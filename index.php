<?php
header('Content-Type: application/json');
// 检测$horseid是否存在
if (empty($_GET['horseid'])) {
    // 如果存在，将其赋值给$horseid
    $horseid = $_GET['horseid'];
} else {
    // 如果不存在，输出json格式的错误信息
    $array= array(
        'code' => '400',
        'msg' => '缺少参数'
    );
    echo json_encode($array, JSON_UNESCAPED_UNICODE);
}
// 正则匹配传入信息只能是数字
if (!preg_match('/^[0-9]+$/', $horseid)) {
    $array = array(
        'code' => '403',
        'msg' => '传入参数错误，仅允许数字传入'
    );
    echo json_encode($array, JSON_UNESCAPED_UNICODE);
    exit;
} else {
    //使用EscapeShellArg和EscapeShellCmd对参数进行转义
    $command = escapeshellcmd(escapeshellarg('python ./core/index.py "' . $horseid . '"'));
    echo $command;
    // 执行python脚本
    $data = exec($command);
}
echo iconv('gbk', 'utf-8', $data);
