import React from 'react';
import { createRoot } from 'react-dom/client';
import { LocalCockpitApp } from './LocalCockpitApp';

const root = document.getElementById('root');

if (root) {
  createRoot(root).render(
    <React.StrictMode>
      <LocalCockpitApp />
    </React.StrictMode>,
  );
}
