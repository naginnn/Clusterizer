import {apiBase, API_URL} from "./apiBase"

const apiConfigureModel = apiBase.injectEndpoints({
    endpoints: (build => ({
        getData: build.query({
            query: () => ({
                url: `${API_URL}/load_data`,
                credentials: "include"
            }),
            transformResponse: (response) => response.questions,
        }),
        uploadData: build.mutation({
            query: (json) => ({
                method: 'POST',
                url: `${API_URL}/upload_data`,
                body: json,
                credentials: "include"
            }),
            transformResponse: (response) => response.questions,
        })
    })),
    overrideExisting: false
})

export const {
    useGetDataQuery,
    useUploadDataMutation,
} = apiConfigureModel
