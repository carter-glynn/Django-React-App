import React from "react"

function Item({item, onDelete}) {
    return (<div>
                <h3>{item.name}</h3>
                <p>Category: {item.category}</p>
                <p>Price: ${item.price}</p>
                <p>Purchase Date: {item.purchase_date}</p>
                <p>Warranty Expiration: {item.warranty_expiration}</p>
                {item.image && (
                    <img
                        src={item.image}
                        alt={item.name}
                        style={{ width: "200px" }}
                    />
                )}<br />
                <button onClick={() => onDelete(item.id)}>Delete</button>
            </div>
    );
}

export default Item