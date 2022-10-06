import { useEffect, useState } from "react";
import { Wrapper } from "./Wrapper";

// Add this in your component file
require('react-dom');
window.React2 = require('react');
console.log(window.React1 === window.React2);
export const Products = () => {
    const [products, setProducts] = useState([]);
    useEffect(() => {
        fetch("http://127.0.0.1:8000/products")
            .then(data => {
                return data.json();
            }).then(data => {
                setProducts(data)
            });
    }, []);
    return <Wrapper>
        <div className="pt-3 pb-2 mb-3 border-bottom">
            <link to={'/create'} className="btn btn-sm btn-outline-secondary">Add</link>
        </div>
        <div class="table-responsive">
            <table class="table table-striped table-sm">
                <thead>
                    <tr>
                        <th scope="col">Id</th>
                        <th scope="col">Name</th>
                        <th scope="col">Price</th>
                        <th scope="col">Quantity</th>
                        <th scope="col">Added_At</th>
                    </tr>
                </thead>
                <tbody>
                    {products.map(product => {
                        return <tr key={product.id}>
                            <td>{product.id}</td>
                            <td>{product.name}</td>
                            <td>{product.price}</td>
                            <td>{product.quantity}</td>
                            <td>{product.added_at}</td>
                            <td>
                                <a href="/#" className="btn btn-sm btn-outline-secondary">
                                    Delete
                                </a>
                            </td>
                        </tr>
                    })}
                </tbody>
            </table>
        </div>
    </Wrapper>;
}