// App.js
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import SignInPage from './components/SignInPage';
import Inventory from './components/InventoryPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<SignInPage />} />
        <Route path="/signin" element={<SignInPage />} />
        <Route path="/inventory" element={<Inventory />} /> 
      </Routes>
    </BrowserRouter>
  );
}

export default App;
