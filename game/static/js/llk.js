// canvas变量
var canvas, ctx
// canvas宽高
var canvasWidth, canvasHeight


// 图片的url
var imageUrl = '/static/image/link/link.jpg'
// 图片
var image
// 图片上图标的的行数
var row = 4
// 图片上图标的的列数
var col = 4
// 图片的宽高
var imageWidth, imageHeight
// 图片上每个图标的宽高
var iconWidth, iconHeight

// 显示图标的行数
var rowCount = 8
// 显示图标的列数
var colCount = 8
// 显示图标之间的间隔，包括上下和左右的间隔
var space = 5
// 选中框的边框宽度
var borderWidth = 3
// icon二位数组 存放显示的图标情况
var iconMap = []
// 当前选中的图标位置列表
var selectedPositions = []
// 连接的图标位置列表
var linkPositions = []


// 序号转换为位置
function numberToPosition(number, colCount) {
    var r = parseInt(number / colCount)
    var c = number % colCount
    return [r, c]
}
// 位置转换为序号
function positionToNumber(position, colCount) {
    return position[0] * colCount + position[1]
}
// 位置转换为中心点坐标
function positionToCoordinate(position) {
    var x = position[1] * (iconWidth + space) + space + iconWidth / 2
    var y = position[0] * (iconHeight + space) + space + iconHeight / 2
    return [x, y]
}
// 初始化
function init() {
    // canvas初始化
    canvas = document.getElementById('link');
    ctx = canvas.getContext('2d');
    var cc = colCount + 2
    var rc = rowCount + 2
    canvasWidth = iconWidth * cc + space * (cc + 1)
    canvasHeight = iconHeight * rc + space * (rc + 1)
    $('#link').attr('width', canvasWidth)
    $('#link').attr('height', canvasHeight)
    $('#canvasDiv').css('width', canvasWidth + 20)
    $('#canvasDiv').css('height', canvasHeight + 20)
    // 初始化iconMap然后绘制
    $.post(
        '/game/llk/icon_map',
        {icon_count: row*col, row_count: rowCount, col_count: colCount},
        function (map) {
            iconMap = map
            // 根据iconMap绘制canvas
            paint()
        },
        'json'
    )
}
// 绘制游戏内容
function paint() {
    // 先清除canvas内容
    ctx.fillStyle = "gray";
    ctx.fillRect(0, 0, canvasWidth, canvasHeight);
    // 绘制选中区域
    selectedPositions.forEach(function (v) {
        var p = numberToPosition(v, colCount)
        paintSelected(p[0], p[1])
    })
    // 绘制icon
    for (var i = 0; i < iconMap.length; i++) {
        for (var j = 0; j < iconMap[i].length; j++) {
            paintOne(i, j)
        }
    }
    if (linkPositions.length != 0) {
        ctx.beginPath()
        ctx.strokeStyle = 'red'
        ctx.lineWidth = 2
        var p = linkPositions[0]
        p = [p[0] + 1, p[1] + 1]
        coordinate = positionToCoordinate(p)
        ctx.moveTo(coordinate[0], coordinate[1])
        for (var i = 1; i < linkPositions.length; i++) {
            p = linkPositions[i]
            p = [p[0] + 1, p[1] + 1]
            coordinate = positionToCoordinate(p)
            ctx.lineTo(coordinate[0], coordinate[1])
        }
        ctx.stroke();
    }
}
// 绘制一个位置的内容
function paintOne(i, j) {
    // 绘制icon
    var ii = i + 1
    var jj = j + 1
    var target_x = jj * (iconWidth + space) + space
    var target_y = ii * (iconHeight + space) + space
    var number = iconMap[i][j]
    if (number == -1) {
        // ctx.fillStyle = '#ccc';
        //ctx.fillRect(target_x - 1, target_y - 1, iconWidth + 2, iconHeight + 2);
    } else {
        var p = numberToPosition(number, col)
        var src_x = p[0] * iconHeight
        var src_y = p[1] * iconWidth
        ctx.drawImage(image, src_x, src_y, iconWidth, iconHeight,
            target_x, target_y, iconWidth, iconHeight);
    }
}
// 绘制一个位置的选中效果
function paintSelected(r, c) {
    // 绘制选中区域
    r++;
    c++;
    var x = c * (iconWidth + space) + (space - borderWidth)
    var y = r * (iconHeight + space) + (space - borderWidth)
    var width = iconWidth + 2 * borderWidth
    var height = iconHeight + 2 * borderWidth
    ctx.fillStyle = "blue";
    ctx.fillRect(x, y, width, height)
}
// canvas点击事件
function canvasClick() {
    // 根据鼠标点击的位置 解析出点击了哪个icon
    canvas = $('#link')[0]
    var x = event.pageX - canvas.getBoundingClientRect().left;
    var y = event.pageY - canvas.getBoundingClientRect().top;
    var c = parseInt(x / (iconWidth + space))
    if (c == 0 || c == colCount + 1 || x < c * (iconWidth + space) + space) {
        return
    }
    var r = parseInt(y / (iconHeight + space))
    if (r == 0 || r == rowCount + 1 || y < r * (iconHeight + space) + space) {
        return
    }
    if (iconMap[r-1][c-1] == -1){
        return
    }
    iconClick(r - 1, c - 1)
    paint()
}
// r,c位置的图标的点击处理
function iconClick(r, c) {
    console.log(r,c)
    // 点击第r行第c个icon处理
    var number = positionToNumber([r, c], colCount)
    var index = $.inArray(number, selectedPositions)
    // 若已选中，移除
    if (index != -1) {
        selectedPositions.splice(index, 1)
        return
    }
    console.log('111')
    // 若该icon未选中，则加入已选位置中
    selectedPositions.push(number)
    // 如选中位置为两个，则判断是否为相同且连通，是则将icon移除
    if (selectedPositions.length == 2) {
        n1 = selectedPositions[0]
        n2 = selectedPositions[1]
        p1 = numberToPosition(n1, colCount)
        p2 = numberToPosition(n2, colCount)
        // console.log(p1, p2)
        if (iconMap[p1[0]][p1[1]] == iconMap[p2[0]][p2[1]]) {
            $.post(
                '/game/llk/connected',
                {
                    icon_map: JSON.stringify(iconMap),
                    p1: JSON.stringify(p1),
                    p2: JSON.stringify(p2)
                },
                function (link_positions) {
                    if(link_positions == false) {
                        return
                    }
                    // 连通后画线 延迟300ms将icon消除
                    linkPositions = link_positions
                    paint()
                    setTimeout(function () {
                        linkPositions = []
                        iconMap[p1[0]][p1[1]] = -1
                        iconMap[p2[0]][p2[1]] = -1
                        // 消除后判断游戏状态
                        //返回true代表胜利，false代表没结束继续游戏，
                        //返回map代表没有连通的了，则将iconMap赋值成返回的打乱后的map
                        $.post(
                            '/game/llk/status',
                            {icon_map: JSON.stringify(iconMap)},
                            function (status) {
                                console.log(status)
                                if(status == true){
                                    alert('you win')
                                    init()
                                }else if(status == false){
                                }else{
                                    iconMap = status
                                    paint()
                                }
                            },
                            'json'
                        )
                        paint()
                    }, 100)
                },
                'json'
            )
        }
        // 无论是否两个icon是否消除，都将选中项移除
        selectedPositions.splice(0, 2)

    }
}

function hint() {
    $.post(
        '/game/llk/hint',
        {icon_map: JSON.stringify(iconMap)},
        function (hint) {
            if (hint == false){
                alert('mei lian de le')
            }else{
                console.log(hint[0][0], hint[0][1], hint[1][0], hint[1][1])
            }
        },
        'json'
    )
}
$(function () {
    // 加载图片获取图片尺寸后 调用init
    image = new Image();
    image.onload = function () {
        //img.onload =null;
        imageWidth = image.width
        imageHeight = image.height
        iconWidth = imageWidth / col
        iconHeight = imageHeight / row
        init()
    }
    image.src = imageUrl;
    // 给canvas绑定点击事件
    $('#link').click(canvasClick)
})