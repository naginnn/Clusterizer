import Box from "@mui/material/Box";
import './pageLayout.css';


export const PageLayout = ({sx, ...props}) => {
    return (
        <Box sx={{...sx}} className='page-wrapper'>
            {props.children}
        </Box>
    )
}