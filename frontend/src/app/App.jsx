import React from 'react';
import {Provider} from "react-redux";

import {MainPage} from "../pages/main/MainPage";
import {store} from "../services/store"

import {createTheme, ThemeProvider} from "@mui/material";
import Box from "@mui/material/Box"

import ErrorBoundary from "./ErrorBoundary";

const theme = createTheme({
    typography: {
        button: {
            textTransform: 'none',
            fontSize: '17px'
        }
    },
    palette: {
        custom: {
            primary: 'rgba(0, 0, 0, 0.6)'
        }
    }
})

// Точка инициализации
function App() {
    return (
        <ErrorBoundary>
            <Box>
                <Provider store={store}>
                    <ThemeProvider theme={theme}>
                        <MainPage/>
                    </ThemeProvider>
                </Provider>
            </Box>
        </ErrorBoundary>
    );
}

export default App;
