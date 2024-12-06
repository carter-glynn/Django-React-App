import React, { useState } from "react";

const FilterForm = ({ onFilterSubmit }) => {
    const [category, setCategory] = useState("");
    const [value, setValue] = useState("");
    const [purchaseDate, setPurchaseDate] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        const filters = { category, value, purchaseDate };
        onFilterSubmit(filters);  // Pass the filter data to the parent component
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="category">Category:</label>
                <input
                    type="text"
                    id="category"
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    placeholder="Enter category"
                />
            </div>
            <div>
                <label htmlFor="value">Value:</label>
                <input
                    type="number"
                    id="value"
                    value={value}
                    onChange={(e) => setValue(e.target.value)}
                    placeholder="Enter minimum value"
                />
            </div>
            <div>
                <label htmlFor="purchaseDate">Purchase Date:</label>
                <input
                    type="date"
                    id="purchaseDate"
                    value={purchaseDate}
                    onChange={(e) => setPurchaseDate(e.target.value)}
                />
            </div>
            <button type="submit">Filter</button>
        </form>
    );
};

export default FilterForm;
