import axios from "axios"
import { ACCESS_TOKEN } from "./constants"

const apiUrl = '/choreo-apis/djangoreact4sa3/backend/v1'

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL : apiUrl
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

export const generateReport = (type) => {
    return api.post(
        "/api/reports/", 
        { type },
        { responseType: "blob" }
    );
};

export default api