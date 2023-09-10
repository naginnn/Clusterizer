import {Paper} from "@mui/material";

export const PaperLayout = ({children, sx, ...props}) => {
    return (
        <Paper
            {...props}
            sx={{
                mt: '20px',
                p: '20px',
                ...sx
            }}
        >
            {children}
        </Paper>
    )
}