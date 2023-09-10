import {PageWrapper} from "./PageWrapper";
import {Box, CircularProgress, Modal} from "@mui/material";
import {CenteredBox} from "./CenteredBox";

export const Loading = () => {
    return (
        <PageWrapper>
            <Modal open>
                <Box>
                    <CenteredBox position='absolute'>
                        <CircularProgress/>
                    </CenteredBox>
                </Box>
            </Modal>
        </PageWrapper>
    )
}