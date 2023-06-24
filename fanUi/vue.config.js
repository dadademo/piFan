const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  chainWebpack: (config) => {
    config.externals({
      'echarts': 'echarts'
    });
  },
  devServer: {
    proxy: {
      '/api': {
        // target: 'https://t2.ainfinit.com/',
        // target: 'https://test.ainfinit.com/',
        target: 'http://192.168.0.104:3001/',
        changeOrigin: true, // target是域名的话，需要这个参数，
        secure: true, // 设置支持https协议的代理
        pathRewrite: {
          '^/api': '/'
        }
      },
    }
  },
})
