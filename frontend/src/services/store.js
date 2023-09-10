import {configureStore} from "@reduxjs/toolkit";
import {apiBase} from "./apiBase";

export const store = configureStore({
    reducer: {
        [apiBase.reducerPath]: apiBase.reducer,
    },
    middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(apiBase.middleware),
    devTools: process.env.NODE_ENV !== 'production'
})