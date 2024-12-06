import { useState, useEffect } from "react";
import api from "../api";
import Item from "../components/Item";
import Report from "../components/Report";
import FilterForm from "../components/FilterForm";
import NotificationForm from "../components/NotificationForm";

function Home() {
    const [userId, setUserId] = useState(null);
    const [loading, setLoading] = useState(true);
    const [items, setItems] = useState([]);
    const [name, setName] = useState("");
    const [category, setCategory] = useState("");
    const [purchase_date, setPurchaseDate] = useState("");
    const [price, setPrice] = useState("");
    const [warranty_expiration, setWarrantyExpiration] = useState("");
    const [image, setImage] = useState(null);

    useEffect(() => {
        getItems(); // Initially fetch all items
    }, []);

    useEffect(() => {
        api.get("/api/user/")
            .then((res) => {
                setUserId(res.data.id); // Set the user ID from the response
                setLoading(false); // Stop loading once user data is fetched
            })
            .catch((err) => {
                console.error("Failed to fetch user ID:", err);
                setLoading(false); // Stop loading even if there's an error
            });
    }, []);

    const getItems = (filters = {}) => {
        api
            .get("/api/items/", { params: filters }) // Send filter params as query
            .then((res) => res.data)
            .then((data) => {
                setItems(data);
                console.log(data);
            })
            .catch((err) => alert(err));
    };

    const handleFilterSubmit = (filters) => {
        getItems(filters); // Apply the filters and fetch the filtered data
    };

    const deleteItem = (id) => {
        api
            .delete(`/api/items/delete/${id}/`)
            .then((res) => {
                if (res.status === 204) {
                    alert("Item deleted!");
                    getItems(); // Refresh the list after deletion
                } else {
                    alert("Failed to delete item.");
                }
            })
            .catch((error) => alert(error));
    };

    const createItem = (e) => {
        e.preventDefault();

        // Prepare form data for the POST request
        const formData = new FormData();
        formData.append("name", name);
        formData.append("category", category);
        formData.append("purchase_date", purchase_date);
        formData.append("price", price);
        formData.append("warranty_expiration", warranty_expiration);
        if (image) formData.append("image", image);

        api
            .post("/api/items/", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            })
            .then((res) => {
                if (res.status === 201) {
                    alert("Item created!");
                    getItems(); // Refresh the item list
                } else {
                    alert("Failed to create item.");
                }
            })
            .catch((err) => {
                console.error(err);
                alert("An error occurred while creating the item.");
            });
    };

    // Show a loading message until the user data is fetched
    if (loading) {
        return <p>Loading user information...</p>;
    }

    // Show an error message if userId couldn't be fetched
    if (!userId) {
        return <p>Error: Unable to fetch user information.</p>;
    }

    return (
        <div>
            <h2>Report Generator</h2>
            <Report />

            <h2>Create an Item</h2>
            <form onSubmit={createItem}>
                <label htmlFor="name">Name:</label>
                <input
                    type="text"
                    id="name"
                    required
                    onChange={(e) => setName(e.target.value)}
                    value={name}
                />
                <label htmlFor="category">Category:</label>
                <input
                    type="text"
                    id="category"
                    onChange={(e) => setCategory(e.target.value)}
                    value={category}
                />
                <label htmlFor="purchase_date">Purchase Date:</label>
                <input
                    type="date"
                    id="purchase_date"
                    required
                    onChange={(e) => setPurchaseDate(e.target.value)}
                    value={purchase_date}
                />
                <label htmlFor="price">Price:</label>
                <input
                    type="number"
                    step="0.01"
                    id="price"
                    required
                    onChange={(e) => setPrice(e.target.value)}
                    value={price}
                />
                <label htmlFor="warranty_expiration">Warranty Expiration:</label>
                <input
                    type="date"
                    id="warranty_expiration"
                    onChange={(e) => setWarrantyExpiration(e.target.value)}
                    value={warranty_expiration}
                />
                <label htmlFor="image">Image:</label>
                <input
                    type="file"
                    id="image"
                    accept="image/*"
                    onChange={(e) => setImage(e.target.files[0])}
                />
                <button type="submit">Submit</button>
            </form>

            {/* Pass userId to the NotificationForm */}
            <h2>Notifications</h2>
            <NotificationForm userId={userId} />

            <h2>Items</h2>
            <FilterForm onFilterSubmit={getItems} />
            <div>
                {items.map((item) => (
                    <Item item={item} onDelete={deleteItem} key={item.id} />
                ))}
            </div>
        </div>
    );
}

export default Home;