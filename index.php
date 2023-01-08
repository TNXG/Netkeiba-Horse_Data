<?php
header('Content-Type: application/json');
$horseid = $_GET['id'];
// 检测$horseid是否存在
if (empty($horseid)) {
    // 如果不存在，输出json格式的错误信息
    $array = array(
        'code' => '400',
        'msg' => '缺少参数'
    );
    echo json_encode($array, JSON_UNESCAPED_UNICODE);
} else {
    // 正则匹配传入信息只能是数字
    if (!preg_match('/^[0-9]+$/', $horseid)) {
        $array = array(
            'code' => '403',
            'msg' => '传入参数错误，仅允许数字传入'
        );
        echo json_encode($array, JSON_UNESCAPED_UNICODE);
    } else {
        $data = exec("python ./core/index.py \"$horseid\"");
        echo iconv('gbk', 'utf-8', $data);
    }
}
