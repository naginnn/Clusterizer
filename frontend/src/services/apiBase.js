import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react";

export const API_URL = process.env.REACT_APP_API_URL

export const apiBase = createApi({
    baseQuery: fetchBaseQuery({baseUrl: API_URL}),
    endpoints: () => ({}),
    refetchOnMountOrArgChange: true,
})
