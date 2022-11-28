// 引用本js文件
// 找到index.html目录: /opt/emby-server/system/dashboard-ui/index.html
// 将index.html文件<body>里面添加两行，jquery去网上下
// <script type="text/javascript" src="./jquery-3.6.0.min.js"></script>
// <script type="text/javascript" src="./emby.js"></script>

// 替换你的alist地址头部
const alistUrl = "https://pan.onerookie.site/d";

//后端处理alist中有密码的video
const flaskUrl = 'https://movie.onerookie.site/api/detail?target='

//在时间内，重复调用addButton按钮函数
const timer1 = setInterval("addButton()", 500);

//Nplaye、potplayer、wangpan按钮
function addButton() {
    var showornot = $("div.mediaSource .sectionTitle div")[0];
    //$('button[data-action="play"]').hide();//屏蔽emby自带的播放按钮
    //$('button[class="btnPlay raised raised-mini listTextButton-autohide emby-button"]').hide();
    //$('button[class="btnShuffle raised raised-mini listTextButton-autohide emby-button"]').hide();
    //根据媒体信息判断是否进入了视频详细页面
    if (showornot) {
        //判断是否添加过按钮了
        var nplayer = $("div[is='emby-scroller']:not(.hide) .nplayer")[0];
        if (!nplayer) {
            var mainDetailButtons = $("div[is='emby-scroller']:not(.hide) .mainDetailButtons")[0];
            if (mainDetailButtons) {
                var html = mainDetailButtons.innerHTML;
                //注入自定义按钮
                //mainDetailButtons.innerHTML = `${html} ${nplayerButton} ${potplayerButton} ${onlineButton}`;
                let buttonhtml = `
                <div class ="flex">
                    <button is="emby-button" id="software" type="button" class="detailButton emby-button software" onclick="window.open('https://pan.onerookie.site/onedrive/Software/media')"> <div class="detailButton-content"> <i class="md-icon detailButton-icon"></i>  <div class="detailButton-text">软件下载</div> </div> </button>
                  <button is="emby-button" id="nplayer" type="button" class="detailButton emby-button nplayer" onclick="nplayeropen()"> <div class="detailButton-content"> <i class="md-icon detailButton-icon"></i>  <div class="detailButton-text">Nplayer播放</div> </div> </button>
                  <button is="emby-button" id="potplayer" type="button" class="detailButton emby-button potplayer" onclick="potplayeropen()"> <div class="detailButton-content"> <i class="md-icon detailButton-icon"></i>  <div class="detailButton-text">Potplayer播放</div> </div> </button>
                    <button is="emby-button" id="wangpan" type="button" class="detailButton emby-button wangpan" onclick="wangpanopen()"> <div class="detailButton-content"> <i class="md-icon detailButton-icon"></i>  <div class="detailButton-text">在线播放</div> </div> </button> 
                  </div>`
                mainDetailButtons.insertAdjacentHTML('afterend', buttonhtml)
                //$("button[title='播放']").hide();
                //$("button[title='预告片']").hide();
                //$("button[title='删除']").hide()
            }
        }
    }
}

//Nplayer按钮。功能
async function nplayeropen() {
    const nplayerUrl = "nplayer-" + await getVideoUrl()
    console.log(nplayerUrl)
    window.open(nplayerUrl)
}

//potplayer按钮。功能
async function potplayeropen() {
    const potplayerUrl = "potplayer://" + await getVideoUrl()
    console.log(potplayerUrl)
    window.open(potplayerUrl)
}

//wangpan按钮。功能
async function wangpanopen() {
    window.open('player.html?target=' + await getVideoPath())
}

async function getVideoUrl() {
    const path = await getVideoPath()
    if (path.indexOf('private') === -1) {
        return alistUrl + path
    }
    let videoUrl = ''
    var ajax = new XMLHttpRequest();
    // true:请求为异步  false:同步
    ajax.onreadystatechange = function () {
        if (ajax.readyState === 4 && ajax.status === 200) {
            var res = JSON.parse(ajax.responseText === "" ? '{}' : ajax.responseText);
            videoUrl = res['true_url'];
        } else return null;
    }
    ajax.open("GET", flaskUrl + itemId, false);
    ajax.send();
    return videoUrl;
}
async function getVideoPath() {
    const userId = ApiClient._serverInfo.UserId
    const itemId = /\?id=(\d*)/.exec(window.location.hash)[1]
    const item = await ApiClient.getItem(userId, itemId)
    let path = item.MediaSources[0].Path
    path = path.replace('/onedrive/od-movie', '/onedrive')
        .replace('/onedrive/ali', '/ali')
    return path
}
