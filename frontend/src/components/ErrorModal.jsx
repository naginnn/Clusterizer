import {CenteredBox} from "./CenteredBox";
import {Typography} from "@mui/material";

import {getErrorMessage} from "../utils/getErrorMessage";

export const ErrorModal = ({error = {} }) => {
    return (
        <CenteredBox
            position="absolute"
            sx={{
                width: '500px',
                height: '300px',
                padding: '50px',
                bgcolor: '#ffffff',
            }}
        >
            <CenteredBox>
                <Typography variant='h5' textAlign='center'>
                    {getErrorMessage(error)}
                </Typography>
            </CenteredBox>
        </CenteredBox>
    )
}