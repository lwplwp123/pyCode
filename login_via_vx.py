# coding:utf-8


# https://open.weixin.qq.com/connect/oauth2/authorize?appid=APPID&redirect_uri=REDIRECT_URI&response_type=code&scope=SCOPE&state=STATE#wechat_redirect
# #这里将redirect_uri配置为当前H5页面
# 参考链接(请在微信客户端中打开此链接体验):
# scope为snsapi_base
# https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx520c15f417810387&redirect_uri=https%3A%2F%2Fchong.qq.com%2Fphp%2Findex.php%3Fd%3D%26c%3DwxAdapter%26m%3DmobileDeal%26showwxpaytitle%3D1%26vb2ctag%3D4_2030_5_1194_60&response_type=code&scope=snsapi_base&state=123#wechat_redirect
# scope为snsapi_userinfo
# https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxf0e81c3bee622d60&redirect_uri=http%3A%2F%2Fnba.bluewebgame.com%2Foauth_response.php&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect

# H5 page.
# <script>
#           // server-address
#           const address = "http://dev.finpin.cn"
#           // api url
#           const Api = {          
#             getUserInfo : `${address}/finance/front/user/regiestUserForOfficial`
#           };

#           $(function(){

#           function getUrlParam(name) {
#             var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)')
#             let url = window.location.href.split('#')[0]
#             let search = url.split('?')[1]
#             if (search) {
#               var r = search.substr(0).match(reg)
#               if (r !== null)
#                 return unescape(r[2])
#               return null
#             } else
#               return null
#           }

          
#           // 获取code
#           const code = getUrlParam('code')  // 截取路径中的code
#           const token = getUrlParam('token') // 截取token
#           if (code == null || code === '') {
#             const local = window.location.href
#             console.log(local)
#             const appid = 'wx4e5ffc96380fdc6f'     
#             // 测试号
#             //const appid = 'wxc9db2ce9f68a9dea'    
#             window.location.href = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid='+appid+'&redirect_uri=' + encodeURIComponent(local) + '&response_type=code&scope=snsapi_base&state=1#wechat_redirect';
            
#           } else {
#             // 获取用户信息
#             $.post(Api.getUserInfo,{code:code,token:token},function(result){

#               // 结果赋值
#               if(result.status == 1){
#                 const { data } = result
#                 $('#userName').html(data.uName)
#                 openId = data.attr1
#                 console.log(result) 
#               }else{
#                 weui.alert('服务器连接失败！'); 
#               }        
#             });
            
#           }       
#         })
#         </script>




