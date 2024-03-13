import React from 'react'
import ReactDOM from 'react-dom/client'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import './index.css'
import SecretView from './routes/secret';
import Login from './routes/login';
import Signup from './routes/signup';

const router = createBrowserRouter([
  {
    path: "/",
    element: <SecretView />,
  },
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/signup",
    element: <Signup />,
  },
]);

import { AuthService } from "@genezio/auth";

// Replace <token> and <region> with your own values
AuthService.getInstance().setTokenAndRegion("0-lr74n76mzx7ftee2zhairrercm0rzhjp", "us-east-1");



ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
  <RouterProvider router={router} />
  </React.StrictMode>,
)
