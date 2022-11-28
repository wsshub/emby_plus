# emby_plus，更优雅地看电影
使用[alist](https://github.com/alist-org/alist)挂载OneDrive、阿里云盘等网盘后，通过alist的webdav功能将其挂载到服务器；  
emby读取文件自动削刮元数据，播放时通过nginx反代播放请求，解析出视频真实链接后返回；  
基于artplayer写个了播放器，可以发弹幕。  
