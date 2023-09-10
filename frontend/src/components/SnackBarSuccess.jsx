import {useState} from "react";

import Portal from '@mui/material/Portal';
import Box from "@mui/material/Box";
import Snackbar from "@mui/material/Snackbar";
import Alert from '@mui/material/Alert';

export const SnackBarSuccess = ({closeHandler, autoHideDuration = 10000, sx, children, ...props}) => {
    const [isError, setIsError] = useState(true);

    const onClose = (event, reason) => {
        if (reason === 'clickaway')
            return

        if (closeHandler) {
            closeHandler()
        }

        setIsError(false)
    }

    return (
        <Portal>
            <Snackbar
                onClick={(e) => e.stopPropagation()}
                {...props}
                onClose={onClose}
                open={isError}
                autoHideDuration={autoHideDuration}
                sx={{...sx}}>
                <Box>
                    <Alert severity="success">
                        {children}
                    </Alert>
                </Box>
            </Snackbar>
        </Portal>
    )
}

export default SnackBarSuccess;