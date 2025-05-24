# Dashboard Frontend

This directory contains the React application used for the web dashboard. It is built on top of the Mantis free React template and uses Material‑UI components with Redux for state management.

## Features

- React 18 with functional components and hooks
- Material‑UI v5 for the UI and theming
- Redux Toolkit and Recoil for state management
- React Router v6 for routing
- Preconfigured ESLint and Prettier
- Unit testing setup with React Testing Library

## Prerequisites

- Node.js 16 or higher
- npm or Yarn package manager

## Getting Started

Install dependencies and start the development server:

```bash
cd front/dashboard
npm install      # or yarn
npm start        # or yarn start
```

Open <http://localhost:3000> to view the app in the browser. The page will reload when you make edits.

## Available Scripts

- `npm start` – Runs the app in development mode
- `npm run build` – Builds the app for production to the `build/` folder
- `npm test` – Launches the test runner
- `npm run eject` – Ejects from Create React App (this action is permanent)

## Environment Variables

Create a `.env` file in the project root to override settings from `package.json` or provide API URLs and other secrets. See the [Create React App documentation](https://create-react-app.dev/docs/adding-custom-environment-variables/) for more details.

## Folder Structure

```
front/dashboard
├── public          # Static assets and HTML template
├── src             # Application source code
│   ├── assets      # Images and fonts
│   ├── components  # Reusable UI components
│   ├── pages       # Route level pages
│   ├── store       # Redux store configuration
│   └── ...         # Other helpers and utilities
```

## Deployment

Run `npm run build` to create a production bundle. Deploy the contents of the `build/` directory to any static hosting service or web server.

## Contributing

Contributions are welcome. Please open an issue or submit a pull request to propose changes.

## License

This project is licensed under the MIT License and incorporates the [Mantis Free React Dashboard](https://github.com/codedthemes/mantis-free-react-admin-template) design.

