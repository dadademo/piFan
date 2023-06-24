import axios from 'axios'
// 创建axios实例
const service = axios.create({
  // baseURL: process.env.BASE_API, // api的base_url
  timeout: 500000 // 请求超时时间
})

// request拦截器
service.interceptors.request.use(
  config => {

    return config
  },
  error => {
    // Do something with request error
    console.log(error) // for debug
    Promise.reject(error)
  }
)

// respone拦截器
service.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.log(error)
    return Promise.reject(error)
  }
)

export default service
