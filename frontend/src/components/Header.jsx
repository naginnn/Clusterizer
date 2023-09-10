import {PageLayout} from "./PageLayout";

import {Box, Grid, Typography} from "@mui/material";

import logo from '../assets/voteLogo.png'

export const Header = () => {
    return (
        <Box
            sx={{
                position: 'relative',
                height: '64px',
                width: '100%',
                bgcolor: 'white',
                zIndex: 1,
            }}
        >
            <PageLayout>
                <Grid
                    container
                    justifyContent='space-between'
                    alignItems='center'
                    m='auto'
                    height='100%'
                    color='#ffffff'
                >
                    <Grid item>
                        <img src={logo} style={{objectFit: 'cover', height: '64px'}} alt='vote logo'/>
                    </Grid>
                    <Grid item>
                        <Typography>
                            Header
                        </Typography>
                        {/*<FocusedTypography*/}
                        {/*    focusColor='#026595'*/}
                        {/*    color='#0e2b46'*/}
                        {/*>*/}
                        {/*    Поиск объектов*/}
                        {/*</FocusedTypography>*/}
                    </Grid>
                </Grid>
            </PageLayout>
        </Box>
    )
}