import React from "react"

import Box from "@mui/material/Box";

export const CenteredBox = ({sx, position = 'relative', children, ...props}) => {
    return (
        <Box
            sx={{
                ...sx,
                position: position,
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
            }}
            {...props}
        >
            {children}
        </Box>
    )
}
