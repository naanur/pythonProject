import axios from "axios";
const API_URL = "http://localhost:8000";

export default class ProductsService {

    constructor(){}

    getProducts(){
        const url = `${API_URL}/api/products/`;
        return axios.get(url).then(response => response.data);
    }


}