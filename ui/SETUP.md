# Quick Setup Guide

## Prerequisites
- Node.js 18+ and npm installed
- Backend API running on `http://localhost:8000`

## Installation Steps

1. **Navigate to the UI directory:**
   ```bash
   cd ui
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Open your browser:**
   Navigate to `http://localhost:4200`

## Features

✨ **Beautiful Tile Layout**
- Each asset displayed as an elegant card
- Color-coded by asset category (Stock, Bond, MTF)
- Hover effects and smooth animations

📊 **Profitability Indicators**
- Visual profitability badges with color coding:
  - Green: High profitability (>10%)
  - Blue: Positive profitability (0-10%)
  - Orange: Neutral (-10% to 0%)
  - Red: Negative (<-10%)

🎨 **Modern Design**
- Gradient purple background
- Glassmorphism effects on cards
- Responsive grid layout
- Mobile-friendly design

🔍 **Interactive Features**
- Search by Customer ID
- Request new recommendations
- Refresh existing recommendations
- Click assets to log interactions
- Real-time status updates

## Troubleshooting

**CORS Issues:**
If you encounter CORS errors, you may need to configure the backend to allow requests from `http://localhost:4200`. Alternatively, you can use a proxy configuration in Angular.

**API Connection:**
Make sure the backend server is running on port 8000. You can test it by visiting `http://localhost:8000/health`

**Port Already in Use:**
If port 4200 is already in use, Angular CLI will automatically try the next available port (4201, 4202, etc.)

