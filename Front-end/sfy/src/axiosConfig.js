import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    console.log(error.response.status)
    if (error.response.status === 401) {
      const refreshToken = localStorage.getItem('refreshToken');
      console.log('i am here')
      try {
        const { data } = await axios.post('http://localhost:8000/api/token/refresh/', {
          refresh: refreshToken,
        });

        localStorage.setItem('accessToken', data.access);
        originalRequest.headers.Authorization = `Bearer ${data.access}`;

        return axios(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
      }
    }
    return Promise.reject(error);
  }
);

export default api;
