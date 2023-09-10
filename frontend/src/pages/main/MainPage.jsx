import {useState, useMemo, useEffect} from "react"

import {Box, Tabs, Tab, Button, Modal, Typography, Portal, CircularProgress} from "@mui/material"
import {useTheme} from '@mui/material/styles';

import {PageWrapper} from "../../components/PageWrapper";
import {PaperLayout} from "../../components/PaperLayout";
import {FileDropArea} from "../../components/FileDropArea";
import {CenteredBox} from "../../components/CenteredBox";
import {Loading} from "../../components/Loading";
import {TreeMapQuestionChart} from "./TreeMapQuestionChart";
import {useGetDataQuery, useUploadDataMutation} from "../../services/clusterApi";
import {normalizeData} from "./normalizeData";
import SnackBarError from "../../components/SnackBarError";
import SnackBarSuccess from "../../components/SnackBarSuccess";

export const MainPage = () => {
    const theme = useTheme();
    const [value, setValue] = useState(0);
    const [showModal, setShowModal] = useState(false)
    const [refetchAfterUpload, setRefetchAfterUpload] = useState(false)
    const {data, refetch, isFetching, isSuccess, error} = useGetDataQuery()
    const [fetchUpload, {
        error: errorUpload,
        isSuccess: successUpload,
        isFetching: fetchingUpload
    }] = useUploadDataMutation()

    useEffect(() => {
        if (!fetchingUpload && successUpload) {
            setRefetchAfterUpload(true)
            setTimeout(() => {
                setRefetchAfterUpload(false)
                refetch()
            }, 8000)
        }
    }, [fetchingUpload, successUpload])

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    const CustomTabPanel = (props) => {
        const {children, value, index, ...other} = props;

        return (
            <div
                role="tabpanel"
                hidden={value !== index}
                id={`simple-tabpanel-${index}`}
                aria-labelledby={`simple-tab-${index}`}
                {...other}
                style={{width: '100%', height: '100%'}}
            >
                {value === index && (
                    <Box sx={{py: '10px', width: '100%', height: "95%"}}>
                        {children}
                    </Box>
                )}
            </div>
        );
    }

    const getPropsTab = (index) => {
        return {
            id: `chart-tab-${index}`,
            'aria-controls': `chart-tabpanel-${index}`,
        };
    }

    const normalizedData = useMemo(() => {
        if (!isFetching && isSuccess) {
            return normalizeData(data)
        }
        return null
    }, [isFetching, isSuccess, data])

    return (
        <PageWrapper>
            <PaperLayout sx={{height: '750px'}}>
                {
                    refetchAfterUpload &&
                    <SnackBarSuccess>Модель обучается, ожидаем новые данные</SnackBarSuccess>
                }
                {
                    error &&
                    <SnackBarError>Не удалось загрузить данные для отображение</SnackBarError>
                }
                {
                    errorUpload &&
                    <SnackBarError>Не удалось загрузить данные для дообучения модели</SnackBarError>
                }
                <Modal
                    open={showModal}
                    onClose={() => setShowModal(false)}
                >
                    <Box>
                        <CenteredBox position='absolute'>
                            <FileDropArea
                                fileFormat='.json'
                                width='500px'
                                height='300px'
                                topic='Поместите данные формата json'
                                submitButtonTopic='Отправить данные'
                                onSubmit={(json) => {
                                    setShowModal(false);
                                    fetchUpload(json)
                                }}
                            />
                        </CenteredBox>
                    </Box>
                </Modal>
                <Box sx={{width: '100%', height: '100%'}}>
                    <Box sx={{
                        borderBottom: 1,
                        borderColor: 'divider',
                        display: 'flex',
                        justifyContent: 'space-between'
                    }}
                    >
                        <Tabs value={value} onChange={handleChange}>
                            <Tab label="Treemap" {...getPropsTab(0)}/>
                            <Tab label="Points" {...getPropsTab(1)}/>
                        </Tabs>
                        <Button
                            onClick={() => setShowModal(true)}
                            sx={{
                                color: 'rgba(0, 0, 0, 0.6)',
                                '&:hover': {
                                    color: theme.palette.primary.main
                                }
                            }}
                        >
                            Загрузить данные
                        </Button>
                    </Box>
                    {
                        (isFetching || !normalizedData || fetchingUpload)
                            ? <Modal open>
                                <CenteredBox position='absolute'>
                                    <CircularProgress/>
                                </CenteredBox>
                            </Modal>
                            : isSuccess &&
                            <>
                                <CustomTabPanel value={value} index={0}>
                                    <TreeMapQuestionChart data={normalizedData}/>
                                </CustomTabPanel>
                                <CustomTabPanel value={value} index={1}>
                                    Dots
                                </CustomTabPanel>
                            </>
                    }

                </Box>
            </PaperLayout>
        </PageWrapper>
    )
}