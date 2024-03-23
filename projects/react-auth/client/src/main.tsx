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
        element: <SecretView/>,
    },
    {
        path: "/login",
        element: <Login/>,
    },
    {
        path: "/signup",
        element: <Signup/>,
    },
    {
        path: "/reset",
        element: <ResetPasswordForm/>,
    }
]);

import {AuthService} from "@genezio/auth";
import ResetPasswordForm from "./routes/reset.tsx";

// Replace <token> and <region> with your own values
AuthService.getInstance().setTokenAndRegion("0-xkux5orerrrqqxcp5vo3zpnczm0qihjh", "us-east-1");


ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
        <RouterProvider router={router}/>
    </React.StrictMode>,
)
