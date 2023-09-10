import Box from "@mui/material/Box";

import {PageLayout} from "./PageLayout";
import {Header} from "./Header";

export const PageWrapper = ({sx, children,...props}) => {
    return (
        <Box sx={{...sx}} {...props}>
            <Header/>
            <PageLayout>
                {children}
            </PageLayout>
        </Box>
    )
}