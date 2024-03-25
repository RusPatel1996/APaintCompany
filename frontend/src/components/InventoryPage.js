import React, { useState } from 'react';
import axios from 'axios';
import { API_URL } from '.';

function InventoryPage() {
    axios.get(API_URL + 'inventory/').then(response => console.log(response.data.user))

    return (
        <div>
            <h2>Inventory</h2>
            
        </div>
    );
}

export default InventoryPage;