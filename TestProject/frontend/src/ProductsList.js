import React, {Component} from 'react';
import ProductsService from "./ProductsService";
import {LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, Scatter, LabelList} from "recharts";

const productsService = new ProductsService();


class ProductsList extends Component {

    constructor(props) {
        super(props);
        this.state = {
            products: [],
            data: [],
            // nextPageURL: ''
        };
        // this.nextPage = this.nextPage.bind(this);
        // this.handleCreate = this.handleCreate.bind(this);

    }


    componentDidMount() {
        let self = this;
        productsService.getProducts().then(function (result) {
            // console.log(result);
            const data = [];

            result.map((item) => {
                data.push({name: item.delivery_time, cost: item.cost, pv: 2400, amt: 2400});
            });

            self.setState({products: result, data: data});
        });
    }

    render() {
        return (

        <div className="products--list">

                <LineChart width={800} height={400} data={this.state.data}>
                    <Line type="monotone" dataKey="cost" stroke="#8884d8"/>
                    <CartesianGrid stroke="#ccc" strokeDasharray="5 5"/>
                    <XAxis dataKey="name" scaleToFit={true}/>
                    <YAxis />
                    <Tooltip/>
                </LineChart>
            <table className="table" width={50}>
                <thead key="thead">
                <tr>
                    <th>id</th>
                    <th>Order #</th>
                    <th>Cost</th>
                    <th>Delivery Time</th>
                    <th>Cost in Rubles</th>
                </tr>
                </thead>
                <tbody>

                {this.state.products.map(c =>
                    <tr key={c.id}>
                        <td>{c.id}</td>
                        <td>{c.order_number}</td>
                        <td>{c.cost}</td>
                        <td>{c.delivery_time}</td>
                        <td>{c.cost_in_rub}</td>
                    </tr>
                )}
                </tbody>
            </table>
            {/*TODO: Add Next Page Link button after pagination API implementation */}
            {/*<button className="btn btn-primary" onClick={this.nextPage}>Next</button>*/}
        </div>
    )
        ;
    }
}

export default ProductsList;