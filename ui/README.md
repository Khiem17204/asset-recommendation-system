# Asset Recommendation UI

A modern Angular application for displaying asset recommendations with a beautiful tile-based interface.

## Features

- 🎨 Modern, responsive design with gradient backgrounds
- 🎯 Tile-based asset display
- 📊 Profitability indicators with color coding
- 🔍 Search by Customer ID
- 📱 Fully responsive for mobile devices
- ⚡ Real-time recommendation fetching
- 🎭 Smooth animations and transitions

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn
- Angular CLI: `npm install -g @angular/cli`

## Installation

1. Install dependencies:
```bash
npm install
```

## Development

Run the development server:
```bash
npm start
```

Navigate to `http://localhost:4200/`

## Build

Build for production:
```bash
npm run build
```

## API Configuration

The UI connects to the backend API at `http://localhost:8000`. Make sure the backend server is running.

To change the API URL, update the `apiUrl` in `src/app/services/recommendation.service.ts`.

## Usage

1. Enter a Customer ID (e.g., `DED5BF19E23CCCFEE322`)
2. Click "Get Recommendations" to request new recommendations
3. Click "Refresh" to reload existing recommendations
4. Click on any asset card to log an interaction

## Technologies

- Angular 17
- Angular Material
- TypeScript
- SCSS
- RxJS

