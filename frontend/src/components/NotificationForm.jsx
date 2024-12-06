import React, { useState, useEffect } from "react";
import api from "../api";

const NotificationForm = () => {
    const [items, setItems] = useState([]);
    const [selectedItem, setSelectedItem] = useState("");
    const [notifyWhen, setNotifyWhen] = useState("");

    useEffect(() => {
        const fetchItems = async () => {
            const response = await api.get("/api/items/");
            setItems(response.data);
        };
        fetchItems();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log("Submitting:", { item: selectedItem, notify_when: notifyWhen }); // Log the data
        try {
            await api.post("/api/set-notification/", {
                item: selectedItem,
                notify_when: notifyWhen,
            });
            alert("Notification preference saved!");
        } catch (error) {
            console.error(error.response || error);
            alert("Failed to save preference.");
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Set Notification Preferences</h2>
            <div>
                <label htmlFor="item">Select Item:</label>
                <select
                    id="item"
                    value={selectedItem}
                    onChange={(e) => setSelectedItem(e.target.value)}
                >
                    <option value="">--Choose an item--</option>
                    {items.map((item) => (
                        <option key={item.id} value={item.id}>
                            {item.name}
                        </option>
                    ))}
                </select>
            </div>
            <div>
                <label htmlFor="notifyWhen">Notify Me:</label>
                <select
                    id="notifyWhen"
                    value={notifyWhen}
                    onChange={(e) => setNotifyWhen(e.target.value)}
                >
                    <option value="">--Choose notification timing--</option>
                    <option value="immediate">Immediately</option>
                    <option value="six_months">6 months before expiry</option>
                    <option value="one_month">1 month before expiry</option>
                    <option value="one_week">1 week before expiry</option>
                    <option value="day_of">On expiry date</option>
                </select>
            </div>
            <button type="submit">Save Notification</button>
        </form>
    );
};

export default NotificationForm;
