# emby_plus，更优雅地看电影
使用[rclone](https://rclone.org/)、[alist](https://github.com/alist-org/alist)挂载OneDrive、阿里云盘等网盘后，通过alist的webdav功能将其挂载到服务器；  
emby读取文件自动削刮元数据，播放时通过nginx反代播放请求，解析出视频真实链接后返回；  
阿里云盘播放速度嘎嘎快，OneDrive加了cloudflare反代后速度也还可以；  
基于artplayer写个了播放器，可以发弹幕。  
  
### 注意事项  
需要在emby用户设置中关闭转码；  
阿里云盘播放需要在emby地index.html中加入"\<meta charset="UTF-8" name="referrer" content="no-referrer">"，参考player.html。

### 目前不足
rclone挂载的OneDrive中的视频emby可以刮到字幕，但是webdav挂载的阿里云盘下的视频挂不到字幕。  
  
![](https://github.com/wsshub/emby_plus/blob/main/emby1.JPG)
![](https://github.com/wsshub/emby_plus/blob/main/emby2.JPG)
![](https://github.com/wsshub/emby_plus/blob/main/emby3.JPG)
